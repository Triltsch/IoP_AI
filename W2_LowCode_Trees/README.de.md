# Woche 2: Low-Code und Entscheidungsbäume

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

Der KNN-Klassifikator aus Woche 1 wird in KNIME (Low-Code) nachgebaut und durch ein gut lesbares Modell ersetzt: einen Entscheidungsbaum. Danach prüfen Sie, wie belastbar das Ergebnis ist, und führen ein eigenes Experiment durch.

## Notebooks (Ordner `en` und `de`)

| Notebook | Thema |
|---|---|
| `04_Decision_Tree_Blockage` | **Entscheidungsbäume:** Genügt eine Schwelle, wie tief darf ein Baum werden, bevor er auswendig lernt, lässt er sich als Regel für die Werkhalle lesen, wie schneidet er gegenüber KNN ab (ca. 40 min, Paare). Endet mit `export_for_knime(k)`, das die Merkmalsdateien für KNIME schreibt |
| `05_Validate_Over_Time` | **Validierung über die Zeit:** nur 34 Blockaden; Zeit-Split gegenüber Zufalls-Split, wandernder Split, helfen zusätzliche Merkmale oder passen sie nur Rauschen an (ca. 35 min, Paare) |
| `06_Own_Experiment` | **Eigenes Experiment:** eine von drei Varianten wählen (Baum und Schwelle, mehr Merkmale, Validierung über die Zeit), eine Sache ändern, das Protokoll ausfüllen (35 min, Paare) |

Jedes Notebook gibt es als `_student` (mit Lücken `___`) und `_solution`.

## Weitere Dateien

- `de/Experiment_Protokoll.md` (`en/Experiment_Protocol.md`): Protokollvorlage zu Notebook 06 (Hypothese, Experiment, Ergebnis, Schlussfolgerung; Pitch von 60 Sekunden).
- `KNIME/`: der Workflow `IoP_W2_Blockage_Tree_{en,de}.knwf` (KNIME 5.4.3) mit einer Kopie der Merkmalsdatei von Drucker 1 sowie die Merkmalsdateien von Drucker 1 und 2.
- `de/KNIME_Workflow_Anleitung.md` (`en/KNIME_Workflow_Guide.md`): Anleitung zum Workflow.

## Daten

`../00_Data/printfarm` (2024/25) und die Merkmalsdateien in `../00_Data/knime`. Siehe die dortigen READMEs.

## Weiter

Woche 3 testet die eingefrorenen Modelle an neuen Druckern und in einem neuen Jahr und macht daraus einen Service.
