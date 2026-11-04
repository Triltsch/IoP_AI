# Print-farm data set 2026 / Druckerfarm-Datensatz 2026

Same scenario as `../printfarm` (2024/25), but **six** printers (0 to 5) and the year 2026. Used for the transfer test and the replay of the monitor in week 3. / Gleiches Szenario wie `../printfarm` (2024/25), aber **sechs** Drucker (0 bis 5) und das Jahr 2026. Verwendet für den Übertragungstest und den Replay des Monitors in Woche 3.

| File | Content / Inhalt |
|---|---|
| `Printer_0.csv` … `Printer_5.csv` | per minute / je Minute: `Timestamp`, `State`, `Temp_Extruder`, `Temp_Bed`, `Filament`, `Total_Power` (cumulative counter / Zählerstand) |
| `Printer_0_error.csv` … `Printer_5_error.csv` | `Timestamp`, `Error` |
| `Printproduction.csv`, `Printproduction_QM_scrap.csv` | orders and defects / Aufträge und Fehler (orders `26xx_nnn`) |

Period: 5 Jan 2026 – 19 Sep 2026 (369,867 minutes per printer). 295 extruder blockages (42 to 57 per printer), few other errors.

**Differences to 2024/25 / Unterschiede zu 2024/25:** time stamps are ISO (`2026-01-05 08:45:21`, seconds = 21) instead of `05.01.2024 08:45`; blockages are much more frequent (class 1 is 8 to 13 % of the printing samples instead of 4 %), connection errors are rare. Semicolon and decimal comma are unchanged. Do not mix the two data sets. / Zeitstempel sind ISO statt `05.01.2024 08:45`; Blockaden sind viel häufiger (Klasse 1 macht 8 bis 13 % der Stichproben aus statt 4 %), Verbindungsabbrüche sind selten. Semikolon und Dezimalkomma sind unverändert. Beide Datensätze nicht mischen.
