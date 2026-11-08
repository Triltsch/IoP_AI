# Week 3: from model to assistant

**🇬🇧 English** · [🇩🇪 Deutsch](README.de.md)

The warning sign of weeks 1 and 2 becomes a tool: it is tested on new printers and a new year, documented, wrapped as a service, and (next step) used in a monitor with a traffic light.

## Notebooks (folders `en` and `de`)

| Notebook | Topic |
|---|---|
| `01_Transfer_Test` | **Transfer test:** the models fitted on printer 1 (2024/25) stay frozen and are tested on the six printers of 2026: announced blockages, false alarms, chance level, drift check, per-printer baseline |
| `02_MLflow_Tracking` | **Experiment tracking:** log runs (parameters, metrics, model), compare them in the MLflow web interface, register the chosen model with a version and the alias `production` |
| `03_Model_Service` | **Model as a service:** start a Flask service that loads the registered model, call it with real data, test bad inputs, check that service and offline pipeline compute the same features, roll out a new version and roll back |

Each notebook exists as `_student` (with gaps) and `_solution`. Run **02 before 03**.

## Files

- `blockage_core.py`: shared code (feature calculation, evaluation, the registered models). Training, service and later the monitor use the same functions, so that training and operation compute the features identically.
- `blockage_service.py`: the model service (`/predict`, `/health`, `/reload`), started by notebook 03.
- `environment.yml`: conda environment (copy in `../binder/environment.yml`).

## Data

The frozen models are fitted on printer 1 of `../00_Data/printfarm` (2024/25) and tested on `../00_Data/printfarm_2026` (6 printers, 2026).

## Notes

- **MLflow web interface on Binder:** notebook 02 starts it and shows a link below the cell (`…/proxy/5000/`). Locally open `http://localhost:5000`.
- `mlflow.db` and `mlartifacts/` are created in this folder when you run notebook 02 (not part of the repository).
- **Next:** OPC UA replay server and monitor with a traffic light (health score: green, yellow, red) as the bridge to the agent block.
