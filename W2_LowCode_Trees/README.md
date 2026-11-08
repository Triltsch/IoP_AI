# Week 2: low-code and decision trees

**🇬🇧 English** · [🇩🇪 Deutsch](README.de.md)

The KNN classifier of week 1 is rebuilt in KNIME (low-code) and replaced by a model that is easy to read: a decision tree. Then you check how reliable the result is and run an experiment of your own.

## Notebooks (folders `en` and `de`)

| Notebook | Topic |
|---|---|
| `04_Decision_Tree_Blockage` | **Decision trees:** is one threshold enough, how deep may a tree be before it memorises, can it be read as a rule for the shop floor, how does it compare with KNN (about 40 min, pairs). Ends with `export_for_knime(k)`, which writes the feature files for KNIME |
| `05_Validate_Over_Time` | **Validation over time:** only 34 blockages; time split versus random split, a moving split, do additional features help or fit noise (about 35 min, pairs) |
| `06_Own_Experiment` | **Own experiment:** choose one of three options (tree and threshold, more features, validation over time), change one thing, fill in the protocol (35 min, pairs) |

Each notebook exists as `_student` (with gaps `___`) and `_solution`.

## Other files

- `en/Experiment_Protocol.md` (`de/Experiment_Protokoll.md`): protocol template for notebook 06 (hypothesis, experiment, result, conclusion; 60-second pitch).
- `KNIME/`: the workflow `IoP_W2_Blockage_Tree_{en,de}.knwf` (KNIME 5.4.3) with a copy of the feature file of printer 1, and the feature files of printers 1 and 2.
- `en/KNIME_Workflow_Guide.md` (`de/KNIME_Workflow_Anleitung.md`): guide to the workflow.

## Data

`../00_Data/printfarm` (2024/25) and the feature files in `../00_Data/knime`. See the READMEs there.

## Next

Week 3 tests the frozen models on new printers and a new year and turns them into a service.
