# Internet of Production – AI part: lab material (new structure)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Triltsch/IoP_AI/main?urlpath=lab)

**EN** Start without installation: click the Binder badge (environment `binder/environment.yml`). Locally: `conda env create -f binder/environment.yml`.
**DE** Start ohne Installation: Binder-Badge anklicken (Umgebung `binder/environment.yml`). Lokal: `conda env create -f binder/environment.yml`.

**EN** One folder per lecture week, one subfolder per language (`en`, `de`). Exercises exist as `_student` (with gaps `___`) and `_solution`. Data live once in `00_Data`.
**DE** Ein Ordner je Vorlesungswoche, darin je Sprache ein Unterordner (`en`, `de`). Übungen gibt es als `_student` (mit Lücken `___`) und `_solution`. Die Daten liegen einmalig in `00_Data`.

| Folder | Content | Status |
|---|---|---|
| `00_Data/printfarm` | Print-farm data set (2024/25): 3 printers, orders, quality control | new, see its README |
| `00_Data/knime` | Feature files for the KNIME workshop (printer 1 and 2: E30, E120, slope, label, train/test) | new, see its README |
| `W1_Data_and_Classification` | Week 1, one thread on the print-farm data: Ex. 1 understand the data and find the warning sign, Ex. 2 predict the extruder blockage (KNN), Ex. 3 which orders fail (and why) | Ex. 1, 2, 3 |
| `W2_LowCode_Trees` | Week 2, same thread: KNIME workshop (tree workflow ready as `KNIME/IoP_W2_Blockage_Tree_en.knwf` / `_de.knwf` for KNIME 5.4.3, KNN built by the students; guide in `KNIME_Workflow_Guide.md` / `KNIME_Workflow_Anleitung.md`), own experiment (notebook 06, three options, protocol template); Ex. 4 decision trees and Ex. 5 validation over time | notebook 06, Ex. 4, 5 and KNIME guide **new**; older tree notebooks (material data) remain in the folder as self-study |
| `W3_Model_to_Assistant` | Week 3: transfer test (printer 1 -> 2), MLflow, model as a service, monitor (see its README) | notebooks 01 to 03 (transfer test, MLflow, model service); monitor in preparation |

## Paths
Notebooks of week 1 read the print-farm data with `DATA = Path('../../00_Data/printfarm')`. Open Jupyter in the folder of the notebook (`.../W1_Data_and_Classification/en`), or keep the folder structure when you hand it out.
