# Print-farm data set (2024/25)

Scenario: print production of a teaching kit for bearings (`PA_Didaktikbaukasten_SoSe25`), three 3D printers (0, 1, 2).
Szenario: Druckfertigung eines Didaktikbaukastens für Lagerungen, drei 3D-Drucker (0, 1, 2).

| File | Content / Inhalt |
|---|---|
| `Printer_0.csv`, `Printer_1.csv`, `Printer_2.csv` | per minute / je Minute: `Timestamp`, `State` (setup, ready, printing, idle, error), `Temp_Extruder`, `Temp_Bed`, `Filament`, `Total_Power` |
| `Printer_0_error.csv` … `Printer_2_error.csv` | `Timestamp`, `Error` (Extruder blocked, Connection interrupted, Empty filament, Crash detected) |
| `Printproduction.csv` | orders: `Order`, `Start`, `BOM Item`, `Material`, `Colour`, `Target Duration`, `Actual Duration`, `Status` (completed / failed), `Printer`, `Lot size`, `Material qty. in g` |
| `Printproduction_QM_scrap.csv` | defects per order: material breakout, support structure remains, under-extrusion, warpage, OK / not OK |

Period: 5 Jan 2024 – 14 May 2025. Time stamps: `day.month.year hour:minute`.

**Note:** `IoP/WS24_25/Data` in the repository holds an older data set (year 2023) with the same file names. Do not mix the two versions.
**Hinweis:** `IoP/WS24_25/Data` im Repository enthält einen älteren Datensatz (Jahr 2023) mit gleichen Dateinamen. Beide Versionen nicht mischen.
