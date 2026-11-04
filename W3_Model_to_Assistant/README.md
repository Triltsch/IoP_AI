# Week 3: from model to assistant (plan, not yet built) / Woche 3: vom Modell zum Assistenten (Plan, noch nicht gebaut)

**Status:** Notebooks 01 to 03 are built; monitor, replay server and slides are in preparation. / Notebooks 01 bis 03 sind gebaut; Monitor, Replay-Server und Folien sind in Vorbereitung.

## Thread / Roter Faden
Week 1: find the warning sign (energy before an extruder blockage) and use it in a KNN classifier on printer 1. Week 3 turns this into a **monitor** that others can use (agent block).
Woche 1: Warnzeichen finden (Energie vor einer Extruder-Blockade) und in einem KNN-Klassifikator für Drucker 1 nutzen. Woche 3 macht daraus einen **Monitor**, den andere nutzen können (Agentenblock).

## Planned sequence / Geplante Abfolge (2 x 90 min, Pause nach Block 5) — revised 29 Oct 2026

Reason: week 1 ran with 150 instead of 180 min and was too full; the rest of week 1 moved into week 2 (see `W2_LowCode_Trees`). Week 3 is reduced to what the monitor needs, with explicit buffer. / Grund: Woche 1 lief mit 150 statt 180 min und war zu voll; der Rest von Woche 1 ist in Woche 2 gewandert. Woche 3 enthält nur noch, was der Monitor braucht, mit Puffer.

| Block | Min | Step | Content | Notebook (planned) |
|---|---|---|---|---|
| 5 | 0–5 | – | Recap of the experiment pitches of week 2 | – |
| 5 | 5–35 | 1 | **Transfer test:** train on printer 1, test on printer 2 (and back). Compare with the **per-printer baseline** (own limit from the reference period, exercise 2b step 6): does a model trained on one printer beat a limit set per printer? | `01_Transfer_Test` |
| 5 | 35–60 | 2 | Experiment tracking with MLflow **on the transfer test** (log printer, feature set, threshold, recall, precision, events); replaces the Iris example | `02_MLflow_Printfarm` |
| 5 | 60–90 | 3 | Model as a service: demo of a prepared Flask API, students call `/predict` with the last minutes of a printer | `03_Model_Service` |
| 6 | 0–5 | – | Recap, what the monitor needs | – |
| 6 | 5–50 | 4 | Monitor: data replay of the minute data (OPC UA), calls the service, uses the orders (which order runs on the printer, expected end) and recommends (service before the next job) | `04_Monitor` |
| 6 | 50–65 | 5 | Handover to the agent block: the monitor as a tool for an assistant (communication method, AI vs rule-based) | see agent block |
| 6 | 65–90 | – | Buffer (also for overrun of step 4) and wrap-up | – |

**Dropped / optional:** time to blockage as regression target (former step 2): only as a demo or take-home, because it is not needed for the monitor. / **Entfällt / optional:** Zeit bis zur Blockade als Regression (früherer Schritt 2): nur als Demo oder Hausaufgabe, da für den Monitor nicht nötig.

**Prepared for students (not built live):** service code and replay server; students edit parameters and call them. If step 3 or 4 runs over, the buffer in block 6 absorbs it; step 5 can be shortened to a discussion.

## Preliminary result for step 1 / Vorläufiges Ergebnis zu Schritt 1
Same pipeline as exercise 2 of week 1 (KNN, k = 25, E30/E120/slope, label "blockage within 6 h"), scaler and model trained on the first 70 % of printer 1, replaced data files of printers 0 and 2:

| Test set | Accuracy | Recall | Precision | AUC | Baseline accuracy |
|---|---|---|---|---|---|
| Printer 1, last 30 % | 97.3 % | 59.0 % | 71.8 % | 0.88 | 95.8 % |
| **Printer 2, whole period (transfer)** | 98.6 % | 55.4 % | 74.4 % | 0.87 | 97.8 % |
| Printer 2, last 30 % (transfer) | 99.5 % | 69.0 % | 87.9 % | 0.85 | 98.9 % |
| Printer 2 → printer 1 (trained on P2, test on P1 whole) | 97.3 % | 58.5 % | 75.7 % | 0.90 | 95.6 % |
| Printer 0 (only 2 blockages, not meaningful) | 99.8 % | 8.8 % | 33.3 % | 0.67 | 99.9 % |

The warning sign transfers between printers 1 and 2. Printer 0 has too few blockages for a statement. Caveat: results of one split, few events, to be checked again when the notebook is built.

## Data and environment / Daten und Umgebung (added 4 Nov 2026)
- **Data 2026:** `00_Data/printfarm_2026` (six printers, 5 Jan to 19 Sep 2026, ISO time stamps, orders included). Training stays on printer 1 of 2024/25 (frozen model), testing is on the six printers of 2026: a genuine forward test on new printers and a new year. / Training bleibt Drucker 1 aus 2024/25 (eingefrorenes Modell), getestet wird auf den sechs Druckern von 2026: ein echter Vorwärtstest an neuen Druckern und in einem neuen Jahr.
- **Environment:** `environment.yml` (conda, Python 3.12; mlflow, flask, asyncua < 2, jupyter-server-proxy). The pool PCs hand over a clean kernel: either create the environment and register it as a kernel, or run the fallback cell `%pip install mlflow flask "asyncua>=1.1.5,<2" nest-asyncio` at the top of the notebook (pip and internet are available at the pool). For Binder copy the file to `binder/environment.yml` of https://github.com/Triltsch/IoP (public); web interfaces such as the MLflow UI are reached through `jupyter-server-proxy` at `/proxy/5000/`. / Die Poolrechner übergeben einen leeren Kernel: entweder Umgebung anlegen und als Kernel registrieren oder die Rückfallzelle `%pip install ...` ganz oben im Notebook ausführen. Für Binder die Datei als `binder/environment.yml` ins Repository kopieren.
- **Monitor:** builds on `Agentensystem/OPC_UA_Communication` (factory server, publish/subscribe): the replay publishes the printer data into `Factory/Machines/Mxx`, the monitor subscribes, calls the model service and writes the traffic light and `Maintenance/Jobs/Mxx_RepairNeeded`. Traffic light: smoothed health score, green to yellow to red. / Der Monitor baut auf dem OPC-UA-Material des Agentensystems auf; Ampel: geglätteter Gesundheitswert, Grün über Gelb nach Rot.

## Result of the transfer test (notebook 01, verified 4 Nov 2026) / Ergebnis des Übertragungstests
Frozen models fitted on the first 70 % of printer 1 (2024/25), applied to the six printers of 2026:

| Model | AUC (range over printers) | Recall | Precision | False alarm episodes / printer / week |
|---|---|---|---|---|
| KNN, k = 25, frozen | 0.86 to 0.89 (mean 0.876) | 50 to 61 % | 68 to 88 % | about 0.5 |
| z-value rule on E120 (95 % quantile, z = 1.79), frozen | 0.89 to 0.94 (mean 0.910) | 64 to 74 % | 61 to 77 % | about 0.5 (0.44 to 0.83) |

- 269 of 295 blockages (91 %, 95 % interval 87 to 94 %) are announced within 6 h by the frozen rule; alarms of the same frequency shifted randomly in time announce 19 % (15 to 23 %).
- The normal level has not moved: mean E120 1.647 to 1.650 Wh/min against 1.645 in the reference.
- A per-printer baseline gives the same AUC (the z-value is a linear transformation of E120); it only moves the limit (own reference: 64 of 73 blockages, 0.38 false episodes per week; frozen: 68 of 73, 0.64).
- Candidate for the opening PI: the share of class 1 is about 10 % in 2026 against 4.4 % in 2024/25; recall (55 % against 59 %) and AUC (0.88 for both) hardly change, precision rises (78 % against 72 %): precision depends on the base rate, recall and AUC do not.

## Open decisions / Offene Entscheidungen
- Regression step: dropped from the plan (demo or take-home only).
- Orders in the monitor: how the order data enter (which order is running, expected end) and what the monitor recommends (service before the next job).
- Agent block: OPC UA with publish/subscribe (decided 4 Nov 2026).
- Orders in the monitor: show the running order; the maintenance recommendation is a traffic light, not an assignment of orders to printers (the 2024/25 diagnosis does not support one).
