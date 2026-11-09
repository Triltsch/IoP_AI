# Woche 3: vom Modell zum Assistenten

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

Das Warnzeichen aus Woche 1 und 2 wird zu einem Werkzeug: Es wird an neuen Druckern und in einem neuen Jahr getestet, dokumentiert, als Service bereitgestellt und in einem Monitor mit Ampel genutzt, der sein Ergebnis nach OPC UA schreibt.

## Notebooks (Ordner `en` und `de`)

| Notebook | Thema |
|---|---|
| `01_Transfer_Test` | **Übertragungstest:** Die an Drucker 1 (2024/25) angepassten Modelle bleiben eingefroren und werden an den sechs Druckern von 2026 getestet: angekündigte Blockaden, Fehlalarme, Zufallsniveau, Drift-Check, Baseline je Drucker |
| `02_MLflow_Tracking` | **Experimentverwaltung:** Läufe protokollieren (Parameter, Metriken, Modell), in der MLflow-Weboberfläche vergleichen, das gewählte Modell mit Version und Alias `production` registrieren |
| `03_Model_Service` | **Modell als Service:** Einen Flask-Service starten, der das registrierte Modell lädt, ihn mit echten Daten aufrufen, fehlerhafte Eingaben testen, prüfen, dass Service und Offline-Pipeline dieselben Merkmale berechnen, eine neue Version ausrollen und zurückrollen |

| `04_Monitor_Traffic_Light` | **Monitor mit Ampel:** Gesundheitswert und Farbschwellen entwerfen, den Monitor auf einem OPC-UA-Replay von 12 Stunden der Druckerfarm (sechs Drucker) laufen lassen, prüfen, welche Blockaden die Ampel angekündigt hat, `RepairNeeded` und die betroffenen Aufträge auslesen |

Jedes Notebook gibt es als `_student` (mit Lücken) und `_solution`. **02 vor 03 und 04** ausführen (sie laden die in 02 registrierten Modelle).

## Dateien

- `blockage_core.py`: gemeinsamer Code (Merkmalsberechnung, Auswertung, die registrierten Modelle). Training, Service und später der Monitor nutzen dieselben Funktionen, damit Training und Betrieb die Merkmale identisch berechnen.
- `blockage_service.py`: der Model-Service (`/predict`, `/health`, `/reload`), wird von Notebook 03 gestartet.
- `replay_server.py`: der Replay-OPC-UA-Server (asyncua). Er spielt die Minutendaten von 2026 mit 1x, 60x oder 600x ab und bietet die Knoten des Fabrik-Servers aus dem Agentenblock (`Factory/Machines/M01 ...`, `Maintenance/Jobs`, `Orders`) plus `Energy`, `SimTime`, `Speed` und `Running`. Wird von Notebook 04 gestartet; er läuft auch allein: `python replay_server.py --help`.
- `monitor_core.py`: der Monitor (OPC-UA-Subscription, Fenster von 360 Druckminuten, Aufrufe des Service, `RepairNeeded`, betroffene Aufträge) und die Auswertungshilfen von Notebook 04. Gesundheitswert und Schwellen schreiben die Studierenden selbst.
- `environment.yml`: Conda-Umgebung (Kopie in `../binder/environment.yml`).

## Daten

Die eingefrorenen Modelle werden an Drucker 1 aus `../00_Data/printfarm` (2024/25) angepasst und an den sechs Druckern aus `../00_Data/printfarm_2026` (2026) getestet.

## Hinweise

- **MLflow-Weboberfläche auf Binder:** Notebook 02 startet sie und zeigt unter der Zelle einen Link (`…/proxy/5000/`). Lokal `http://localhost:5000` öffnen.
- Beim Ausführen von Notebook 02 werden `mlflow.db` und `mlartifacts/` in diesem Ordner angelegt (nicht Teil des Repositorys).
- Notebook 04 startet den Replay-Server auf Port 4840 (der Endpunkt des Fabrik-Servers aus dem Agentenblock) und den Service auf Port 5005. Beenden Sie beide mit der letzten Zelle, sonst bleiben die Ports belegt.
- `replay.log` und `service.log` entstehen in diesem Ordner (nicht Teil des Repositorys). Wenn ein Start scheitert, zeigt das Notebook das Ende dieser Logs.
