# Druckerfarm-Datensatz (2024/25)

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

Szenario: Druckfertigung eines Didaktikbaukastens für Lagerungen (`PA_Didaktikbaukasten_SoSe25`), drei 3D-Drucker (0, 1, 2).

| Datei | Inhalt |
|---|---|
| `Printer_0.csv`, `Printer_1.csv`, `Printer_2.csv` | je Minute: `Timestamp`, `State` (setup, ready, printing, idle, error), `Temp_Extruder`, `Temp_Bed`, `Filament`, `Total_Power` |
| `Printer_0_error.csv` … `Printer_2_error.csv` | `Timestamp`, `Error` (Extruder blocked, Connection interrupted, Empty filament, Crash detected) |
| `Printproduction.csv` | Aufträge: `Order`, `Start`, `BOM Item`, `Material`, `Colour`, `Target Duration`, `Actual Duration`, `Status` (completed / failed), `Printer`, `Lot size`, `Material qty. in g` |
| `Printproduction_QM_scrap.csv` | Fehler je Auftrag: Materialausbruch, Stützstruktur bleibt, Unterextrusion, Verzug, i. O. / n. i. O. |

Zeitraum: 5. Jan 2024 – 14. Mai 2025. Zeitstempel: `Tag.Monat.Jahr Stunde:Minute`.

**Hinweis:** `IoP/WS24_25/Data` im Repository enthält einen älteren Datensatz (Jahr 2023) mit gleichen Dateinamen. Beide Versionen nicht mischen.
