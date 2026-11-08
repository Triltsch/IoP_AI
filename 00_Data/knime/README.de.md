# KNIME-Merkmalsdateien

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

`blockage_features_printer1.csv`, `blockage_features_printer2.csv`: eine Zeile je 10. Druckminute; Spalten `Timestamp, E30, E120, slope, y, label, split` (kommagetrennt, Dezimalpunkt). `y` = 0/1, `label` = ok/warn (Extruder-Blockade innerhalb von 6 h), `split` = train für die ersten 70 % in der Zeit.

Erzeugt mit `export_for_knime(k)` am Ende von `W2_LowCode_Trees/*/04_Decision_Tree_Blockage_*.ipynb` (EN/DE). Drucker 2 ist für den Übertragungstest in Woche 3 gedacht (alle Zeilen als Testdaten verwenden). Der Workflow `W2_LowCode_Trees/KNIME/IoP_W2_Blockage_Tree_*.knwf` (KNIME 5.4.3) enthält eine Kopie der Datei von Drucker 1.
