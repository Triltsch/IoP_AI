# Druckerfarm-Datensatz 2026

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

Gleiches Szenario wie `../printfarm` (2024/25), aber **sechs** Drucker (0 bis 5) und das Jahr 2026. Verwendet für den Übertragungstest und den Replay des Monitors in Woche 3.

| Datei | Inhalt |
|---|---|
| `Printer_0.csv` … `Printer_5.csv` | je Minute: `Timestamp`, `State`, `Temp_Extruder`, `Temp_Bed`, `Filament`, `Total_Power` (Zählerstand) |
| `Printer_0_error.csv` … `Printer_5_error.csv` | `Timestamp`, `Error` |
| `Printproduction.csv`, `Printproduction_QM_scrap.csv` | Aufträge und Fehler (Aufträge `26xx_nnn`) |

Zeitraum: 5. Jan 2026 – 19. Sep 2026 (369.867 Minuten je Drucker). 295 Extruder-Blockaden (42 bis 57 je Drucker), wenige andere Fehler.

**Unterschiede zu 2024/25:** Die Zeitstempel sind ISO (`2026-01-05 08:45:21`, Sekunden = 21) statt `05.01.2024 08:45`; Blockaden sind viel häufiger (Klasse 1 macht 8 bis 13 % der Druck-Stichproben aus statt 4 %), Verbindungsabbrüche sind selten. Semikolon und Dezimalkomma sind unverändert. Beide Datensätze nicht mischen.
