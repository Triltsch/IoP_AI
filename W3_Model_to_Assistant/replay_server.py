"""Replay OPC UA server of week 3: plays the minute data of the print farm 2026 as if it were live.

    python replay_server.py --data ../00_Data/printfarm_2026 --start "2026-01-28 12:00" --hours 12 --speed 600

The information model is the one of the factory server of the agent block (same namespace URI, same browse paths),
so that the agents can connect to it without changes:

    Objects/Factory/Machines/M01 ... M06     Temperature (extruder, deg C), State, Busy, and new: Energy (Wh in the last minute)
    Objects/Factory/Maintenance/Jobs         M01_RepairNeeded ... (Boolean, written by the monitor)
    Objects/Factory/Orders/O0001 ...         TargetMachine, State, Priority, DueTime, and new: OrderNo (id in the data set)
    Objects/Factory/SimTime                  simulated time (ISO string)
    Objects/Factory/Speed                    simulated minutes per real minute (writable: 1, 60, 600 ...)
    Objects/Factory/Running                  Boolean: False pauses the replay (writable); with --hold the server starts paused

Printer k of the data set is machine M{k+1:02d}. Every simulated minute all values of all machines are written with the
simulated time as SourceTimestamp, so that a client can order the values even at high speed.
"""
import argparse
import asyncio
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from asyncua import Server, ua

FACTORY_NS_URI = 'http://ostfalia.de/ipt/factory'
ENDPOINT = 'opc.tcp://localhost:4840/freeopcua/server/'
log = logging.getLogger('replay-server')


def load_window(folder, start, hours):
    """Minute data of all printers for [start, start + hours): one DataFrame per printer (State, Temp_Extruder, E in Wh per minute)."""
    folder = Path(folder)
    start = pd.Timestamp(start)
    end = start + pd.Timedelta(hours=hours)
    frames = {}
    k = 0
    while (folder / f'Printer_{k}.csv').exists():
        d = pd.read_csv(folder / f'Printer_{k}.csv', sep=';', decimal=',', usecols=['Timestamp', 'State', 'Temp_Extruder', 'Total_Power'], low_memory=False).dropna(how='all')
        d['Timestamp'] = pd.to_datetime(d['Timestamp'])
        d = d.set_index('Timestamp')
        d['E'] = d['Total_Power'].diff() * 1000               # Wh per minute (the file holds a cumulative counter in kWh)
        frames[k] = d.loc[(d.index >= start) & (d.index < end), ['State', 'Temp_Extruder', 'E']]
        k += 1
    if not frames:
        raise FileNotFoundError(f'no Printer_<k>.csv in {folder}')
    return frames


def load_orders(folder, start, hours):
    """Orders that run during the window, with machine name, start, due time and end."""
    o = pd.read_csv(Path(folder) / 'Printproduction.csv', sep=';')
    o['Start'] = pd.to_datetime(o['Start'])
    o['End'] = o['Start'] + pd.to_timedelta(o['Actual Duration'], unit='m')
    o['Due'] = o['Start'] + pd.to_timedelta(o['Target Duration'], unit='m')
    start = pd.Timestamp(start)
    end = start + pd.Timedelta(hours=hours)
    o = o[(o['End'] > start) & (o['Start'] < end)].sort_values('Start').reset_index(drop=True)
    o['Machine'] = o['Printer'].map(lambda k: f'M{int(k) + 1:02d}')
    return o


def dv(value, vtype, ts=None):
    """DataValue with the simulated time as SourceTimestamp."""
    return ua.DataValue(ua.Variant(value, vtype), SourceTimestamp=None if ts is None else ts.tz_localize('UTC').to_pydatetime())


class ReplayServer:
    def __init__(self, folder, start, hours, speed, endpoint=ENDPOINT, hold=False):
        self.folder, self.start, self.hours, self.speed0, self.endpoint, self.hold = Path(folder), pd.Timestamp(start), hours, float(speed), endpoint, hold
        self.frames = load_window(folder, start, hours)
        self.orders = load_orders(folder, start, hours)
        self.server = Server()
        self.machines, self.jobs, self.order_nodes = {}, {}, {}

    async def build(self):
        await self.server.init()
        self.server.set_endpoint(self.endpoint)
        self.server.set_server_name('Replay OPC UA Server (print farm 2026)')
        ns = self.ns = await self.server.register_namespace(FACTORY_NS_URI)
        objects = self.server.nodes.objects
        self.factory = await objects.add_object(ns, 'Factory')
        machines_folder = await self.factory.add_folder(ns, 'Machines')
        maintenance = await self.factory.add_object(ns, 'Maintenance')
        jobs_folder = await maintenance.add_folder(ns, 'Jobs')
        self.orders_folder = await self.factory.add_folder(ns, 'Orders')
        self.sim_time = await self.factory.add_variable(ns, 'SimTime', str(self.start), ua.VariantType.String)
        self.speed = await self.factory.add_variable(ns, 'Speed', self.speed0, ua.VariantType.Double)
        await self.speed.set_writable()
        self.running = await self.factory.add_variable(ns, 'Running', not self.hold, ua.VariantType.Boolean)
        await self.running.set_writable()
        for k in self.frames:
            name = f'M{k + 1:02d}'
            obj = await machines_folder.add_object(ns, name)
            nodes = {'Temperature': await obj.add_variable(ns, 'Temperature', 20.0, ua.VariantType.Double),
                     'State': await obj.add_variable(ns, 'State', 'ready', ua.VariantType.String),
                     'Busy': await obj.add_variable(ns, 'Busy', False, ua.VariantType.Boolean),
                     'Energy': await obj.add_variable(ns, 'Energy', 0.0, ua.VariantType.Double)}
            for n in nodes.values():
                await n.set_writable()
            self.machines[name] = nodes
            job = await jobs_folder.add_variable(ns, f'{name}_RepairNeeded', False, ua.VariantType.Boolean)
            await job.set_writable()
            self.jobs[name] = job

    async def _create_order(self, i, row):
        oid = f'O{i + 1:04d}'
        obj = await self.orders_folder.add_object(self.ns, oid)
        v = {'TargetMachine': await obj.add_variable(self.ns, 'TargetMachine', row['Machine'], ua.VariantType.String),
             'State': await obj.add_variable(self.ns, 'State', 'RUNNING', ua.VariantType.String),
             'Priority': await obj.add_variable(self.ns, 'Priority', 0, ua.VariantType.Int32),
             'DueTime': await obj.add_variable(self.ns, 'DueTime', row['Due'].to_pydatetime(), ua.VariantType.DateTime),
             'OrderNo': await obj.add_variable(self.ns, 'OrderNo', str(row['Order']), ua.VariantType.String)}
        for n in v.values():
            await n.set_writable()
        self.order_nodes[oid] = v
        return oid

    async def run(self):
        await self.build()
        index = next(iter(self.frames.values())).index
        pending, running = list(self.orders.index), {}                 # orders not yet started / running: id -> row index
        async with self.server:
            log.info('Replay server at %s: %s, %d minutes, %d orders', self.endpoint, self.start, len(index), len(self.orders))
            loop = asyncio.get_running_loop()
            t_next = loop.time()
            for pos, ts in enumerate(index):
                while not await self.running.read_value():                              # paused (or waiting for the monitor)
                    await asyncio.sleep(0.2)
                    t_next = loop.time()
                for i in [i for i in pending if self.orders.loc[i, 'Start'] <= ts]:      # orders start
                    pending.remove(i)
                    running[await self._create_order(i, self.orders.loc[i])] = i
                for oid, i in list(running.items()):                                     # orders end
                    if self.orders.loc[i, 'End'] <= ts:
                        await self.order_nodes[oid]['State'].write_value(self.orders.loc[i, 'Status'].upper(), ua.VariantType.String)
                        del running[oid]
                for k, d in self.frames.items():
                    r = d.iloc[pos]
                    n = self.machines[f'M{k + 1:02d}']
                    e = 0.0 if pd.isna(r['E']) else float(r['E'])
                    await n['Temperature'].write_value(dv(float(r['Temp_Extruder']), ua.VariantType.Double, ts))
                    await n['State'].write_value(dv(str(r['State']), ua.VariantType.String, ts))
                    await n['Busy'].write_value(dv(r['State'] == 'printing', ua.VariantType.Boolean, ts))
                    await n['Energy'].write_value(dv(e, ua.VariantType.Double, ts))      # last: a client can read the others when Energy arrives
                await self.sim_time.write_value(str(ts))
                speed = max(float(await self.speed.read_value()), 0.01)
                t_next += 60.0 / speed
                await asyncio.sleep(max(0.0, t_next - loop.time()))
            log.info('End of the data window reached; the server keeps running.')
            while True:
                await asyncio.sleep(1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--data', default='../00_Data/printfarm_2026')
    ap.add_argument('--start', default='2026-01-28 12:00')
    ap.add_argument('--hours', type=float, default=12)
    ap.add_argument('--speed', type=float, default=600, help='simulated minutes per real minute: 1, 60 or 600')
    ap.add_argument('--endpoint', default=ENDPOINT)
    ap.add_argument('--hold', action='store_true', help='start paused; a client sets Factory/Running = True')
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
    logging.getLogger('asyncua').setLevel(logging.WARNING)
    asyncio.run(ReplayServer(a.data, a.start, a.hours, a.speed, a.endpoint, a.hold).run())
