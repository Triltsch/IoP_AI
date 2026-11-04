# KNIME 5.4.3: the blockage warning as a low-code workflow (week 2, block 3)

**Goal:** run a decision tree on the blockage features in KNIME and add a KNN yourself. About 55 min, in pairs.
**Files:** `IoP_W2_Blockage_Tree_en.knwf` (workflow, with the data inside) and `blockage_features_printer1.csv` (the same data, in `00_Data/knime`). Columns: `Timestamp, E30, E120, slope, y, label, split`; `label` is `ok` / `warn` (blockage within 6 h); comma separated, decimal point. The file is the result of the pipeline of week 1 (rolling means, label, every 10th printing minute).

## Open the workflow
*File > Import KNIME Workflow… > Select file* `IoP_W2_Blockage_Tree_en.knwf`. The workflow contains the nodes below, connected and configured. Execute with *Shift+F7* (all nodes).
If **CSV Reader** is red: double-click, choose the file (`blockage_features_printer1.csv`), OK.

## Part B: decision tree (prepared)
`CSV Reader` → `Column Filter` (keeps E30, E120, slope, label) → `Partitioning` (70 % **from top** = oldest data for training; no random sampling) → `Decision Tree Learner` (class `label`, Gini, *min number records per node = 200*) → `Decision Tree Predictor` (test partition) → `Scorer`. `Decision Tree View (JavaScript)` shows the tree.
1. Execute all; open the Scorer (*Accuracy statistics*): recall and precision of class `warn`.
2. Open the tree view: which feature is at the root, which threshold?
3. Change *min number records per node* to 20 and to 2 (Learner dialog). What happens to the tree and to the result on the test partition?

## Part A: KNN (you build it)
4. **Normalizer** (Z-score, columns E30, E120, slope) at the training partition (first output of `Partitioning`).
5. **Normalizer (Apply)**: model output of the Normalizer + the test partition (second output of `Partitioning`). *Why must the test data use the parameters of the training data?*
6. **K Nearest Neighbor**: normalised training table at port 1, normalised test table at port 2; class column `label`, k = 25.
7. **Scorer** on the KNN output (reference `label`, prediction column of the KNN node).

**Reference (Python, exercises 2 and 4):** KNN k = 25: accuracy 97.3 %, recall 59.0 %, precision 71.8 %; tree with depth 3, balanced class weights: recall 80 %, precision 36 %. The KNIME tree has no class weights and no depth limit; its recall will be lower than that of the balanced Python tree. `Partitioning` takes 70 % of 23,270 rows (16,289 for training); the Python notebooks use 16,288.

## Questions for the discussion
- Which model was faster to build, which easier to explain? Where did you miss code (rolling means, label)?
- What would be needed to build the feature file in KNIME (Lag Column, Moving Aggregation, GroupBy)? Why was it prepared?
- Which steps would have to run again in operation (week 3), and which only once?
