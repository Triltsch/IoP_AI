# Woche 1: Daten und Klassifikation

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

Ausgangspunkt des roten Fadens: Sie lernen die Daten der 3D-Druckerfarm kennen, finden das Warnzeichen vor einer Extruder-Blockade (die Energie je Minute steigt) und machen daraus einen Klassifikator und einen Anomalie-Detektor.

## Notebooks (Ordner `en` und `de`)

| Notebook | Thema |
|---|---|
| `01_Understand_Data` | **Daten verstehen:** einen Drucker laden und bereinigen, Besonderheiten herausfinden, nach einem Warnzeichen vor einer Störung suchen (ca. 55 min, Paare) |
| `02_Predict_Blockage` | **Blockade mit KNN vorhersagen:** Label „Blockade innerhalb von 6 Stunden“, drei Energie-Merkmale, Zeit-Split, Skalierung, Metriken (ca. 25 min, Paare) |
| `02b_Anomaly_Detection` | **Anomalieerkennung ohne Labels:** das normale Verhalten aus den ersten 70 % der Daten lernen und mit einer z-Wert-Regel alarmieren; das Label dient nur zur Auswertung (ca. 20 min, Paare) |
| `03_Failed_Orders` | **Welche Aufträge scheitern?** Klassifikatoren auf den Auftragsdaten, mit den richtigen Metriken beurteilt, drei Sätze Rat für die Leitung der Arbeitsvorbereitung (ca. 25 min, Gruppen zu 2–3) |
| `03b_Diagnosis_Questions` | **Was können die Daten zum *Warum* sagen?** Durchgerechnetes Beispiel zu den sechs Diagnosefragen der Gruppenarbeit (nur Lösung) |

Jede Übung gibt es als `_student` (mit Lücken `___`) und `_solution`. `02_Predict_Blockage_instructor` ist die Dozentenfassung mit den vorbereiteten Schritten.

## Daten

`../00_Data/printfarm` (2024/25, 3 Drucker). Siehe die dortige README.

## Weiter

Woche 2 baut auf derselben Pipeline Entscheidungsbäume und prüft, wie belastbar das Ergebnis ist.
