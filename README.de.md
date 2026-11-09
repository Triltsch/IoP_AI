# Internet of Production – KI-Teil: Übungsmaterial

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Triltsch/IoP_AI/HEAD?urlpath=lab)

Praktische Übungen zum KI-Teil der Vorlesung *Internet of Production* (Ostfalia Hochschule). Ein roter Faden durch alle drei Wochen: **eine 3D-Druckerfarm warnt vor einer Extruder-Blockade**. Sie finden das Warnzeichen in den Daten, bauen und validieren Modelle und machen das Ergebnis zu einem Service und einem Monitor, den andere nutzen können.

## Start

- **Ohne Installation:** Binder-Badge oben anklicken (Umgebung: `binder/environment.yml`). Der erste Start kann einige Minuten dauern.
- **Lokal:** `conda env create -f binder/environment.yml`, dann `conda activate iop-w3` und den Kernel registrieren:
  `python -m ipykernel install --user --name iop-w3 --display-name "Python (iop-w3)"`

## Aufbau

Ein Ordner je Vorlesungswoche, darin je Sprache ein Unterordner (`en`, `de`). Übungen gibt es als `_student` (mit Lücken `___`) und `_solution`. Die Daten liegen einmalig in `00_Data`.

| Ordner | Inhalt |
|---|---|
| `W1_Data_and_Classification` | **Woche 1:** 01 Daten verstehen und Warnzeichen finden; 02 Blockade vorhersagen (KNN, Metriken); 02b Anomalieerkennung mit z-Wert-Regel; 03 welche Aufträge scheitern; 03b Diagnosefragen |
| `W2_LowCode_Trees` | **Woche 2:** 04 Entscheidungsbäume; 05 Validierung über die Zeit; 06 eigenes Experiment (drei Varianten, Protokollvorlage); KNIME-Workflow (`KNIME/`, für KNIME 5.4.3) mit Anleitung |
| `W3_Model_to_Assistant` | **Woche 3:** 01 Transfertest (neue Drucker, neues Jahr); 02 Experiment-Tracking mit MLflow; 03 Modell als Service (Flask). 04 Monitor mit Ampel auf einem OPC-UA-Replay (siehe dortige README) |
| `00_Data/printfarm` | Druckerfarm 2024/25: 3 Drucker, Minutendaten, Fehlerlisten, Aufträge und Qualitätskontrolle (siehe dortige README) |
| `00_Data/printfarm_2026` | Druckerfarm 2026: 6 Drucker (3 neue), 5. Jan bis 19. Sep 2026 (siehe dortige README) |
| `00_Data/knime` | Merkmalsdateien für den KNIME-Workshop (E30, E120, Steigung, Label) |
| `binder/` | Umgebung für Binder und lokale Nutzung |

## Pfade

Die Notebooks lesen die Daten über relative Pfade, z. B. `Path('../../00_Data/printfarm')`. Öffnen Sie Jupyter im Ordner des Notebooks (zum Beispiel `W1_Data_and_Classification/de`) oder behalten Sie die Ordnerstruktur bei.

## Empfohlene Reihenfolge

Woche 1 → Woche 2 → Woche 3. In Woche 3 zuerst Notebook 02, dann 03 (03 lädt die in 02 registrierten Modelle).
