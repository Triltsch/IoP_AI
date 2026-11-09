"""Monitor of week 3: reads the replay OPC UA server, asks the model service and shows a traffic light per machine.

The design decisions that students make themselves (health score and traffic-light thresholds) are passed in as functions:

    update(health, alarm) -> new health         smoothing of the minute alarms
    light(health)        -> 'green' | 'yellow' | 'red'

The rest (subscription, windows of 360 printing minutes, calls to the service, RepairNeeded, orders concerned) is given here.
"""
import asyncio
from collections import deque

import numpy as np
import pandas as pd
import requests
from asyncua import Client, ua

FACTORY_NS_URI = 'http://ostfalia.de/ipt/factory'
WINDOW = 360                                    # printing minutes that the service needs
COLORS = {'green': '#2e9e44', 'yellow': '#f2c200', 'red': '#d62828', 'warm-up': '#b8b8b8', 'error': '#222222'}


async def subscribe_every_sample(sub, node, queuesize=5000):
    """Report every sample of a node, also when the value is equal to the one before.

    The default of OPC UA reports only changes of the value. The energy of a minute is often equal to the one before,
    so we ask for every new time stamp (DataChangeTrigger.StatusValueTimestamp). The queue keeps the samples if the server is fast.
    """
    flt = ua.DataChangeFilter()
    flt.Trigger = ua.DataChangeTrigger.StatusValueTimestamp
    return await sub._subscribe(node, ua.AttributeIds.Value, flt, queuesize)


class _Handler:
    def __init__(self, monitor):
        self.monitor = monitor

    def datachange_notification(self, node, val, data):
        ts = data.monitored_item.Value.SourceTimestamp
        self.monitor._on_value(node.nodeid, pd.Timestamp(ts).tz_convert('UTC').tz_localize(None), val)


class Monitor:
    def __init__(self, opc_url, service_url, update, light, model='zrule'):
        self.opc_url, self.service_url, self.update, self.light, self.model = opc_url, service_url, update, light, model
        self.http = requests.Session()
        self.machines = {}                      # name -> state dict
        self.log = []                           # one row per machine and minute
        self.events = []                        # (simulated time, machine, text)
        self._nodeinfo, self._pending, self._tasks = {}, {}, set()
        self.client = None
        self.sim_time = None

    # ---------------------------------------------------------------- connection
    def prime(self, folder, start):
        """Fill the windows with the last 360 printing minutes before `start` from the data archive (the historian), so that the monitor can judge from the first minute."""
        from pathlib import Path
        start = pd.Timestamp(start)
        k = 0
        self.primed = {}
        while (Path(folder) / f'Printer_{k}.csv').exists():
            d = pd.read_csv(Path(folder) / f'Printer_{k}.csv', sep=';', decimal=',', usecols=['Timestamp', 'State', 'Total_Power'], low_memory=False).dropna(how='all')
            d['Timestamp'] = pd.to_datetime(d['Timestamp'])
            d = d[d['Timestamp'] < start].set_index('Timestamp')
            e = (d['Total_Power'].diff() * 1000)[d['State'] == 'printing'].dropna()
            self.primed[f'M{k + 1:02d}'] = e.iloc[-WINDOW:].tolist()
            k += 1
        return self

    async def start(self, go=True):
        self.client = Client(url=self.opc_url)
        await self.client.connect()
        ns = await self.client.get_namespace_index(FACTORY_NS_URI)
        factory = await self.client.nodes.objects.get_child([f'{ns}:Factory'])
        machines = await factory.get_child([f'{ns}:Machines'])
        jobs = await factory.get_child([f'{ns}:Maintenance', f'{ns}:Jobs'])
        self.orders = await factory.get_child([f'{ns}:Orders'])
        self.ns = ns
        self.speed_node = await factory.get_child([f'{ns}:Speed'])
        self.time_node = await factory.get_child([f'{ns}:SimTime'])
        sub = await self.client.create_subscription(100, _Handler(self))
        for m in await machines.get_children():
            name = (await m.read_browse_name()).Name
            self.machines[name] = {'buf': deque(getattr(self, 'primed', {}).get(name, []), maxlen=WINDOW), 'health': 0.0, 'light': 'warm-up', 'in_error': False, 'state': '',
                                   'z': float('nan'), 'ts': None, 'job': await jobs.get_child([f'{ns}:{name}_RepairNeeded'])}
            for attr in ('Energy', 'State'):
                node = await m.get_child([f'{ns}:{attr}'])
                self._nodeinfo[node.nodeid] = (name, attr)
                await subscribe_every_sample(sub, node)
        if go:                                                        # release the replay (server started with --hold)
            await (await factory.get_child([f'{ns}:Running'])).write_value(True)
        return self

    async def set_speed(self, minutes_per_minute):
        """Change the replay speed while it runs (1, 60, 600 ...): the speed is a node of the server."""
        await self.speed_node.write_value(ua.DataValue(ua.Variant(float(minutes_per_minute), ua.VariantType.Double)))

    async def stop(self):
        for t in list(self._tasks):
            t.cancel()
        await self.client.disconnect()

    # ---------------------------------------------------------------- one minute of one machine
    def _on_value(self, nodeid, ts, val):
        name, attr = self._nodeinfo[nodeid]
        slot = self._pending.setdefault((name, ts), {})
        slot[attr] = val
        if 'Energy' in slot and 'State' in slot:                      # both values of this minute are there
            del self._pending[(name, ts)]
            self._minute(name, ts, slot['State'], float(slot['Energy']))

    def _later(self, coro):
        t = asyncio.ensure_future(coro)
        self._tasks.add(t)
        t.add_done_callback(self._tasks.discard)

    def _minute(self, name, ts, state, energy):
        s = self.machines[name]
        s['state'], s['ts'] = state, ts
        if state == 'error':                                          # the event has happened: no new evidence
            if not s['in_error']:
                s['in_error'] = True
                self.events.append((ts, name, 'ERROR: printer stopped (light was %s)' % s['light']))
            s['light'] = 'error'
        else:
            if s['in_error']:                                         # repaired: new reference situation
                s['in_error'], s['health'], s['light'] = False, 0.0, 'warm-up'
                s['buf'].clear()
                self._later(s['job'].write_value(False))
                self.events.append((ts, name, 'back in operation, health score reset'))
            if state == 'printing':
                s['buf'].append(energy)
                if len(s['buf']) == WINDOW:
                    r = self.http.post(f'{self.service_url}/predict', json={'energy': list(s['buf']), 'model': self.model}, timeout=5).json()
                    s['z'] = r['score']
                    s['health'] = self.update(s['health'], r['alarm'])
                    new = self.light(s['health'])
                    if new == 'red' and s['light'] != 'red':
                        self._later(self._on_red(name, ts))
                    elif new != 'red' and s['light'] == 'red':
                        self._later(s['job'].write_value(False))
                        self.events.append((ts, name, 'light back to %s: RepairNeeded = False' % new))
                    s['light'] = new
        self.log.append((ts, name, state, energy, s['z'], s['health'], s['light']))

    async def _on_red(self, name, ts):
        """Light turns red: set RepairNeeded and find the orders that run on this machine."""
        await self.machines[name]['job'].write_value(True)
        hit = []
        for o in await self.orders.get_children():
            vals = {(await v.read_browse_name()).Name: await v.read_value() for v in await o.get_children()}
            if vals.get('TargetMachine') == name and vals.get('State') == 'RUNNING':
                hit.append(f"{(await o.read_browse_name()).Name} ({vals.get('OrderNo')}, due {vals.get('DueTime'):%H:%M})")
        self.events.append((ts, name, 'RED: RepairNeeded = True; orders concerned: ' + (', '.join(hit) or 'none')))

    # ---------------------------------------------------------------- display and evaluation
    def dataframe(self):
        return pd.DataFrame(self.log, columns=['time', 'machine', 'state', 'energy', 'z', 'health', 'light'])

    def html(self):
        rows = ''.join(
            f"<td style='padding:4px 14px;text-align:center'><div style='font-weight:bold'>{n}</div>"
            f"<div style='width:34px;height:34px;border-radius:50%;margin:4px auto;background:{COLORS[s['light']]}'></div>"
            f"<div style='font-size:12px'>{s['state'] or '-'}<br>health {s['health']:.2f}</div></td>" for n, s in sorted(self.machines.items()))
        t = max((s['ts'] for s in self.machines.values() if s['ts'] is not None), default=None)
        return f"<div style='font-family:sans-serif'><b>Simulated time: {t}</b><table><tr>{rows}</tr></table></div>"


def announced(log, window_h=6):
    """For every transition into the error state: did the light turn red in the window before it (after the last repair), and how long before?

    'scored' is False if the monitor was blind in that window (warm-up after a repair or after a restart).
    """
    out = []
    for name, g in log.groupby('machine'):
        g = g.reset_index(drop=True)
        is_err = g['state'] == 'error'
        for i in g.index[is_err & ~is_err.shift(fill_value=False)]:
            t_err = g.loc[i, 'time']
            earlier = g.loc[:i - 1]
            prev_end = earlier.loc[earlier['state'] == 'error', 'time'].max() if (earlier['state'] == 'error').any() else pd.Timestamp.min
            before = earlier[(earlier['time'] > prev_end) & (earlier['time'] >= t_err - pd.Timedelta(hours=window_h))]
            red = before[before['light'] == 'red']
            out.append({'machine': name, 'error at': t_err, 'first red': red['time'].iloc[0] if len(red) else pd.NaT,
                        'lead [h]': round((t_err - red['time'].iloc[0]).total_seconds() / 3600, 1) if len(red) else None,
                        'announced': bool(len(red)), 'scored': bool((before['light'] != 'warm-up').any())})
    return pd.DataFrame(out)


def offline_evaluation(alarm, blockages, update, light, window_h=6, gap_h=8):
    """The traffic light on a stored alarm series (one value per printing minute, index = time stamp) of one printer.

    Returns the share of blockages with a red light in the window before them, the median lead time in hours and the red episodes
    without a blockage within gap_h hours (false red) per week. After a blockage the health score starts again at 0.
    """
    times, vals = alarm.index, alarm.values
    bl = list(pd.to_datetime(blockages))
    j, health, prev_light = 0, 0.0, 'green'
    red_runs, red_since, red_start = [], None, None
    for t, a in zip(times, vals):
        while j < len(bl) and t > bl[j]:
            health, j = 0.0, j + 1
            if red_start is not None:
                red_runs.append((red_start, bl[j - 1])); red_start = None
            prev_light = 'green'
        health = update(health, a)
        cur = light(health)
        if cur == 'red' and prev_light != 'red':
            red_start = t
        if cur != 'red' and prev_light == 'red' and red_start is not None:
            red_runs.append((red_start, t)); red_start = None
        prev_light = cur
    if red_start is not None:
        red_runs.append((red_start, times[-1]))
    leads, hit = [], 0
    for b in bl:
        runs = [r for r in red_runs if r[0] <= b and r[1] >= b - pd.Timedelta(hours=window_h)]
        if runs:
            hit += 1
            leads.append((b - min(r[0] for r in runs)).total_seconds() / 3600)
    false = [r for r in red_runs if not any(r[0] <= b <= r[0] + pd.Timedelta(hours=gap_h) for b in bl)]
    weeks = (times[-1] - times[0]).total_seconds() / (7 * 86400)
    return {'announced': hit, 'blockages': len(bl), 'share': hit / max(len(bl), 1), 'median lead [h]': float(np.median(leads)) if leads else float('nan'),
            'false red per week': len(false) / weeks}
