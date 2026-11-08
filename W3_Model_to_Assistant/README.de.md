# Woche 3: vom Modell zum Assistenten

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

Das Warnzeichen aus Woche 1 und 2 wird zu einem Werkzeug: Es wird an neuen Druckern und in einem neuen Jahr getestet, dokumentiert, als Service bereitgestellt und (nächster Schritt) in einem Monitor mit Ampel genutzt.

## Notebooks (Ordner `en` und `de`)

| Notebook | Thema |
|---|---|
| `01_Transfer_Test` | **Übertragungstest:** Die an Drucker 1 (2024/25) angepassten Modelle bleiben eingefroren und werden an den sechs Druckern von 2026 getestet: angekündigte Blockaden, Fehlalarme, Zufallsniveau, Drift-Check, Baseline je Drucker |
| `02_MLflow_Tracking` | **Experimentverwaltung:** Läufe protokollieren (Parameter, Metriken, Modell), in der MLflow-Weboberfläche vergleichen, das gewählte Modell mit Version und Alias `production` registrieren |
| `03_Model_Service` | **Modell als Service:** Einen Flask-Service starten, der das registrierte Modell lädt, ihn mit echten Daten aufrufen, fehlerhafte Eingaben testen, prüfen, dass Service und Offline-Pipeline dieselben Merkmale berechnen, eine neue Version ausrollen und zurückrollen |

Jedes Notebook gibt es als `_student` (mit Lücken) und `_solution`. **02 vor 03** ausführen.

## Dateien

- `blockage_core.py`: gemeinsamer Code (Merkmalsberechnung, Auswertung, die registrierten Modelle). Training, Service und später der Monitor nutzen dieselben Funktionen, damit Training und Betrieb die Merkmale identisch berechnen.
- `blockage_service.py`: der Model-Service (`/predict`, `/health`, `/reload`), wird von Notebook 03 gestartet.
- `environment.yml`: Conda-Umgebung (Kopie in `../binder/environment.yml`).

## Daten

Die eingefrorenen Modelle werden an Drucker 1 aus `../00_Data/printfarm` (2024/25) angepasst und an den sechs Druckern aus `../00_Data/printfarm_2026` (2026) getestet.

## Hinweise

- **MLflow-Weboberfläche auf Binder:** Notebook 02 startet sie und zeigt unter der Zelle einen Link (`…/proxy/5000/`). Lokal `http://localhost:5000` öffnen.
- Beim Ausführen von Notebook 02 werden `mlflow.db` und `mlartifacts/` in diesem Ordner angelegt (nicht Teil des Repositorys).
- **Folgt:** OPC-UA-Replay-Server und Monitor mit Ampel (Gesundheitswert: grün, gelb, rot) als Brücke zum Agentenblock.
