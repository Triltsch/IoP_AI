# KNIME 5.4.3: die Blockade-Warnung als Low-Code-Workflow (Woche 2, Block 3)

**Ziel:** In KNIME einen Entscheidungsbaum auf den Blockade-Merkmalen ausführen und ein KNN selbst ergänzen. Etwa 55 min, in Zweiergruppen.
**Dateien:** `IoP_W2_Blockage_Tree_de.knwf` (Workflow, Daten sind enthalten) und `blockage_features_printer1.csv` (dieselben Daten, in `00_Data/knime`). Spalten: `Timestamp, E30, E120, slope, y, label, split`; `label` ist `ok` / `warn` (Blockade innerhalb von 6 h); Komma-getrennt, Dezimalpunkt. Die Datei ist das Ergebnis der Pipeline aus Woche 1 (gleitende Mittelwerte, Label, jede 10. Druckminute).

## Workflow öffnen
*File > Import KNIME Workflow… > Select file* `IoP_W2_Blockage_Tree_de.knwf`. Der Workflow enthält die folgenden Knoten, verbunden und konfiguriert. Alles ausführen mit *Shift+F7*.
Ist der **CSV Reader** rot: Doppelklick, Datei `blockage_features_printer1.csv` wählen, OK.

## Teil B: Entscheidungsbaum (vorbereitet)
`CSV Reader` → `Column Filter` (behält E30, E120, slope, label) → `Partitioning` (70 % **von oben** = älteste Daten zum Training; keine zufällige Auswahl) → `Decision Tree Learner` (Klasse `label`, Gini, *min number records per node = 200*) → `Decision Tree Predictor` (Testpartition) → `Scorer`. `Decision Tree View (JavaScript)` zeigt den Baum.
1. Alles ausführen; Scorer öffnen (*Accuracy statistics*): Recall und Precision der Klasse `warn`.
2. Baumansicht öffnen: Welches Merkmal steht an der Wurzel, welcher Schwellwert?
3. *Min number records per node* auf 20 und auf 2 ändern (Dialog des Learners). Was passiert mit dem Baum und mit dem Ergebnis auf der Testpartition?

## Teil A: KNN (selbst bauen)
4. **Normalizer** (Z-Score, Spalten E30, E120, slope) an die Trainingspartition (erster Ausgang von `Partitioning`).
5. **Normalizer (Apply)**: Modellausgang des Normalizers + Testpartition (zweiter Ausgang von `Partitioning`). *Warum müssen die Testdaten die Parameter der Trainingsdaten verwenden?*
6. **K Nearest Neighbor**: normalisierte Trainingstabelle an Port 1, normalisierte Testtabelle an Port 2; Klassenspalte `label`, k = 25.
7. **Scorer** am KNN-Ausgang (Referenz `label`, Vorhersagespalte des KNN-Knotens).

**Referenz (Python, Übungen 2 und 4):** KNN k = 25: Accuracy 97,3 %, Recall 59,0 %, Precision 71,8 %; Baum Tiefe 3 mit ausgeglichenen Klassengewichten: Recall 80 %, Precision 36 %. Der KNIME-Baum hat weder Klassengewichte noch eine Tiefenbegrenzung; sein Recall wird niedriger sein als beim ausgeglichenen Python-Baum. `Partitioning` nimmt 70 % von 23.270 Zeilen (16.289 zum Training); die Python-Notebooks nutzen 16.288.

## Fragen für die Diskussion
- Welches Modell war schneller gebaut, welches leichter zu erklären? Wo haben Sie Code vermisst (gleitende Mittelwerte, Label)?
- Was wäre nötig, um die Merkmalsdatei selbst in KNIME zu bauen (Lag Column, Moving Aggregation, GroupBy)? Warum war sie vorbereitet?
- Welche Schritte müssten im Betrieb (Woche 3) immer wieder laufen, welche nur einmal?
