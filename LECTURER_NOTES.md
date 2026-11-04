# Lecturer notes – weeks 1 and 2 (not for students / nicht für Studierende)

## Thread of week 1
Ex. 1 find the warning sign in the minute data -> Ex. 2 use it (KNN, process data) -> Ex. 3 order data and why orders fail (link to disturbances). Week 3 brings process data and orders together in one monitor.

## Exercise 1 – key finding
Printer 1, mean energy per minute while printing (Wh/min, unit assumed kWh): normal 1.645; before an extruder blockage it rises steadily from 1.654 (12 h before) to 1.718 (last hour), about +4 %. Single minutes scatter by about 0.14 Wh. Connection interrupted (1.642) and empty filament (1.633) show no rise. Printers 0 and 2 (checked with the replaced files `Printer_0_neu` / `Printer_2_neu`): the same rise. Printer 2 (18 blockages): last 6 h before 1.693 Wh/min vs 1.643 for random printing windows (about 19 standard errors), profile 1.655 (12 h before) to 1.724 (last hour), all 17 evaluable events above the normal range. Printer 0 has only 2 blockages (last 6 h: 1.673 Wh/min, last hour 1.709). Connection interrupted and empty filament show no rise on any printer. All blockages of all three printers occur in the state printing. Consequence: the early warning is not specific to printer 1; a model trained on printer 1 can be tested on printer 2 (transfer test, candidate for week 3). The failures other than extruder blockages (connection interrupted, empty filament, crash) show no precursor in the energy signal.

Note on the data: in the replaced files only the column `Total_Power` differs from the earlier files (states, temperatures and time stamps are identical; the counter stays monotonic with the same step values and the same consumption per state). The earlier version of printers 0 and 2 had no such rise.

## Exercise 2 – reference results (`02_Predict_Blockage_solution`)
Label: extruder blockage within the next 360 min; samples: every 10th printing minute of printer 1 (23,270; 4.4 % class 1); time split 70/30, test 6,982 samples (293 class 1, 11 blockages).

| Model | Accuracy | Recall | Precision |
|---|---|---|---|
| Baseline: never warn | 95.8 % | 0 % | – |
| KNN k = 5, all three features | 96.9 % | 54.9 % | 65.2 % |
| KNN k = 25, all three features | 97.3 % | 59.0 % | 71.8 % |
| KNN k = 75, all three features | 97.4 % | 59.7 % | 73.2 % |
| KNN k = 25, E120 only | 97.2 % | 60.1 % | 69.6 % |
8 of the 11 test blockages are announced by at least one warning in the 6 hours before.

## Exercise 3 – reference results (`03_Failed_Orders_solution`, time split 70/30)
Train 813 orders (89 failed), test 349 orders (45 failed, 12.9 %). Majority baseline: accuracy 87.1 %, recall 0 %.

| Model (features known at order start) | Accuracy | Recall | Precision |
|---|---|---|---|
| Decision tree, depth 8, balanced | 69.3 % | 48.9 % | 20.8 % |
| Decision tree, depth 10 | 71.9 % | 44.4 % | 21.5 % |
| KNN, k = 3 / 5 | 84.8 % / 86.0 % | 2 % / 4 % | 10 % / 25 % |
| Rule "parts 2a and 1a fail" | 57.9 % | 62.2 % | 17.7 % |
| **Leaky**: tree depth 5 with `Actual Duration` and `Material qty. in g` | 98.9 % | 91.1 % | 100 % |

Step 10: all 134 failed orders coincide with a disturbance of their printer (tolerance 5 min), none of the 1,028 completed orders does: 64 connection interrupted, 54 extruder blocked (34 on printer 1), 15 empty filament, 1 crash. Message: order data describe the risk only indirectly; the cause is the disturbance.

## Week 2 – thread and reference results
Timing (revised 29 Oct 2026 after week 1 ran with 150 min; the rest of week 1 moved here; session of 180 min with a break after 90 min).
Block A (0-90): 0-15 PI on KNN (W1 deck, two PI slides: k = 1 on training data -> practically 100 % (99.97 %), test 95.9 %; k = 25, 3 of 25 neighbours class 1 -> majority vote, threshold 0.5) · 15-25 accuracy deceives / metrics (W1 deck) · 25-55 Ex. 2b (4 steps, steps 5-6 optional) · 55-65 leakage, why orders fail, exit question (W1 deck; Ex. 3 is optional) · 65-80 from KNN to tree, low-code, KNIME surface (W2 deck) · 80-90 buffer.
Block B (after the break, 90): 0-5 recap and experiment options · 5-45 KNIME workshop (40, tree branch ready; if short: only task B) · 45-80 own experiment (notebook 06, protocol `Experiment_Protocol.md` / `Experiment_Protokoll.md`) · 80-87 pitch (60 s per pair) · 87-90 outlook. Exit question optional.
Reference slides after the protocol belong to the options: 1 (depth sweep, threshold table), 2 (temperature feature), 3 (random against time split, variation over time). Notebooks 04 and 05 are reference / self-study; notebook 06 holds the pipeline and one section per option.
Ex. 4 and 5 below remain valid as reference results. Materials: deck `Slides/Internet_Of_Production_AI_W2_en.pptx` / `..._KI_W2_de.pptx` (21 slides).

Same pipeline as Ex. 2 (printer 1, label blockage within 360 min, every 10th printing minute, time split 70/30, test 6,982 samples, 293 of class 1).
| Model | Accuracy | Recall | Precision | AUC (test) |
|---|---|---|---|---|
| Rule E120 > 1.68 | 97.0 % | 63.5 % | 64.6 % | 0.905 (E120 as score) |
| Stump (threshold 1.678) | 96.7 % | 64.8 % | 60.5 % | 0.815 |
| Tree depth 3, min leaf 200, balanced | 93.1 % | 80.2 % | 35.5 % | 0.886 |
| KNN k = 25 | 97.3 % | 59.0 % | 71.8 % | 0.884 |
Depth sweep (test AUC): 0.815 / 0.873 / 0.877 / 0.879 / 0.800 / 0.761 / 0.676 / 0.711 for depth 1, 2, 3, 4, 6, 8, 12, none (training AUC up to 1.0). Threshold table on E120: 1.66: recall 84 %, precision 27 %; 1.67: 76 / 50; 1.68: 64 / 65; 1.69: 55 / 78; 1.70: 30 / 84. Feature importance of the small tree: E120 96 %.
Ex. 5: recall time split / random split: 1-NN 0.53 / 0.60, unrestricted tree 0.45 / 0.58, small balanced tree 0.80 / 0.84, KNN 25 0.59 / 0.59. Five time blocks (small tree): recall 0.79, 0.99, 0.76, 0.89, 0.68 with 10, 3, 5, 7, 5 blockages (mean 0.82); AUC energy only 0.893 (0.864, 0.992, 0.854, 0.939, 0.814), with temperatures 0.922 (+0.019, -0.007, +0.061, +0.018, +0.056). Mean temperatures: E120 1.643 against 1.687 Wh/min, bed 90.15 against 90.23 degC before a blockage (not steady with the time to the event, so treated as an unconfirmed hypothesis; test on printer 2 in week 3). The KNIME file for printer 2 has a different class share (2.2 % class 1).
Pitfalls: the "random split looks better" effect is moderate here (smooth features); the 0.99 recall of block 2 rests on 3 events.

## Pitfalls to be found in exercise 1
- Semicolon separator and decimal comma.
- Completeness (step 3): all three files have 713,742 rows, one per minute, no gaps, no empty rows. (The earlier versions of printers 0 and 2 were padded with empty rows up to the Excel limit; the replaced files are not.)
- `Total_Power` is a cumulative counter; energy per minute is its difference (printing about 0.0016, other states about 0.0008 per minute; unit assumed kWh).
- A disturbance starts with `State = error`; error episodes of printer 1: 50, median 747 min, a quarter 20 min or shorter (short and long episodes differ).

## Data versions
This data set (2024/25) differs from `IoP/WS24_25/Data` (2023). The slides and notebooks use 2024/25.

## Open points
- Week 1 flow (new): Ex. 2 steps 1-3 are prepared in the notebook (students read and explain); gaps start in step 5. Ex. 3 (failed orders) is optional; its findings are on the W1 slides "Beware of leakage" and "Why do orders really fail?". Ex. 2b was trimmed to 4 steps; Isolation Forest and printer 2 are optional (printer 2 own baseline is used in week 3).
- Week 3 plan (revised, see `W3_Model_to_Assistant/README.md`): transfer test with per-printer baseline, MLflow on the transfer test, model service, monitor with replay and orders, handover; regression dropped.
- KNIME workflow: tree branch generated, KNN branch left to the students, not yet tested in KNIME; the week 3 notebooks are not yet created.
