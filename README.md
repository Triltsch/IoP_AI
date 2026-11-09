# Internet of Production – AI part: lab material

**🇬🇧 English** · [🇩🇪 Deutsch](README.de.md)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Triltsch/IoP_AI/HEAD?urlpath=lab)

Hands-on exercises of the AI part of the lecture *Internet of Production* (Ostfalia University of Applied Sciences). One thread runs through all three weeks: **a 3D-printer farm warns before an extruder blockage**. You find the warning sign in the data, build and validate models, and turn the result into a service and a monitor that others can use.

## Start

- **Without installation:** click the Binder badge above (environment: `binder/environment.yml`). The first start can take a few minutes.
- **Locally:** `conda env create -f binder/environment.yml`, then `conda activate iop-w3` and register the kernel:
  `python -m ipykernel install --user --name iop-w3 --display-name "Python (iop-w3)"`

## Structure

One folder per lecture week, one subfolder per language (`en`, `de`). Exercises exist as `_student` (with gaps `___`) and `_solution`. The data live once in `00_Data`.

| Folder | Content |
|---|---|
| `W1_Data_and_Classification` | **Week 1:** 01 understand the data and find the warning sign; 02 predict the blockage (KNN, metrics); 02b anomaly detection with a z-value rule; 03 which orders fail; 03b diagnosis questions |
| `W2_LowCode_Trees` | **Week 2:** 04 decision trees; 05 validation over time; 06 own experiment (three options, protocol template); KNIME workflow (`KNIME/`, for KNIME 5.4.3) with guide |
| `W3_Model_to_Assistant` | **Week 3:** 01 transfer test (new printers, new year); 02 experiment tracking with MLflow; 03 model as a service (Flask). 04 monitor with a traffic light on an OPC UA replay (see its README) |
| `00_Data/printfarm` | Print farm 2024/25: 3 printers, minute data, error lists, orders and quality control (see its README) |
| `00_Data/printfarm_2026` | Print farm 2026: 6 printers (3 new), 5 Jan to 19 Sep 2026 (see its README) |
| `00_Data/knime` | Feature files for the KNIME workshop (E30, E120, slope, label) |
| `binder/` | Environment for Binder and local use |

## Paths

Notebooks read the data with relative paths, e.g. `Path('../../00_Data/printfarm')`. Open Jupyter in the folder of the notebook (for example `W1_Data_and_Classification/en`) or keep the folder structure.

## Recommended order

Week 1 → week 2 → week 3. In week 3 run notebook 02 before 03 (03 loads the models registered in 02).
