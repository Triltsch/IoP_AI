# Week 3: from model to assistant / Woche 3: vom Modell zum Assistenten

**EN** The warning sign of weeks 1 and 2 becomes a tool: it is tested on new printers and a new year, documented, wrapped as a service, and (next step) used in a monitor with a traffic light.
**DE** Das Warnzeichen aus Woche 1 und 2 wird zu einem Werkzeug: Es wird an neuen Druckern und in einem neuen Jahr getestet, dokumentiert, als Service bereitgestellt und (nächster Schritt) in einem Monitor mit Ampel genutzt.

## Notebooks (folders `en` and `de`)
| Notebook | Topic / Thema |
|---|---|
| `01_Transfer_Test` | **Transfer test / Übertragungstest:** the models fitted on printer 1 (2024/25) stay frozen and are tested on the six printers of 2026: announced blockages, false alarms, chance level, drift check, per-printer baseline |
| `02_MLflow_Tracking` | **Experiment tracking / Experimentverwaltung:** log runs (parameters, metrics, model), compare them in the MLflow web interface, register the chosen model with a version and the alias `production` |
| `03_Model_Service` | **Model as a service / Modell als Service:** start a Flask service that loads the registered model, call it with real data, test bad inputs, check that service and offline pipeline compute the same features, roll out a new version and roll back |

Each notebook exists as `_student` (with gaps) and `_solution`. Run **02 before 03**. / Jedes Notebook gibt es als `_student` (mit Lücken) und `_solution`. **02 vor 03** ausführen.

## Files / Dateien
- `blockage_core.py`: shared code (feature calculation, evaluation, the registered models). Training, service and later the monitor use the same functions, so that training and operation compute the features identically. / Gemeinsamer Code (Merkmalsberechnung, Auswertung, die registrierten Modelle).
- `blockage_service.py`: the model service (`/predict`, `/health`, `/reload`), started by notebook 03. / Der Model-Service, wird von Notebook 03 gestartet.
- `environment.yml`: conda environment (copy in `../binder/environment.yml`). / Conda-Umgebung.

## Data / Daten
Frozen models are fitted on printer 1 of `../00_Data/printfarm` (2024/25) and tested on `../00_Data/printfarm_2026` (6 printers, 2026). / Die eingefrorenen Modelle werden an Drucker 1 aus 2024/25 angepasst und an den sechs Druckern von 2026 getestet.

## Notes / Hinweise
- **MLflow web interface on Binder:** notebook 02 starts it and shows a link below the cell (`…/proxy/5000/`). Locally open `http://localhost:5000`. / Auf Binder zeigt Notebook 02 nach dem Start einen Link unter der Zelle; lokal `http://localhost:5000`.
- `mlflow.db` and `mlartifacts/` are created in this folder when you run notebook 02 (not part of the repository). / Beim Ausführen von Notebook 02 werden `mlflow.db` und `mlartifacts/` in diesem Ordner angelegt (nicht Teil des Repositorys).
- **Next / Folgt:** OPC UA replay server and monitor with a traffic light (health score: green, yellow, red) as the bridge to the agent block. / OPC-UA-Replay-Server und Monitor mit Ampel als Brücke zum Agentenblock.
