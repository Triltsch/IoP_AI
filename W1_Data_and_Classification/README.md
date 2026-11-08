# Week 1: data and classification

**🇬🇧 English** · [🇩🇪 Deutsch](README.de.md)

Starting point of the thread: you get to know the data of the 3D-printer farm, find the warning sign before an extruder blockage (the energy per minute rises), and turn it into a classifier and into an anomaly detector.

## Notebooks (folders `en` and `de`)

| Notebook | Topic |
|---|---|
| `01_Understand_Data` | **Understand the data:** load and clean one printer, find out what is special about it, look for a warning sign before a disturbance (about 55 min, pairs) |
| `02_Predict_Blockage` | **Predict the blockage with KNN:** label "blockage within 6 hours", three energy features, time split, scaling, metrics (about 25 min, pairs) |
| `02b_Anomaly_Detection` | **Anomaly detection without labels:** learn normal behaviour from the first 70 % of the data and raise an alarm with a z-value rule; the label is used only to evaluate (about 20 min, pairs) |
| `03_Failed_Orders` | **Which orders will fail?** Classifiers on the order data, judged with the right metrics, three sentences of advice for the head of pre-production (about 25 min, groups of 2–3) |
| `03b_Diagnosis_Questions` | **What can the data say about *why*?** Worked example for the six diagnosis questions of the group activity (solution only) |

Each exercise exists as `_student` (with gaps `___`) and `_solution`. `02_Predict_Blockage_instructor` is the lecturer version with the prepared steps.

## Data

`../00_Data/printfarm` (2024/25, 3 printers). See the README there.

## Next

Week 2 builds decision trees on the same pipeline and checks how reliable the result is.
