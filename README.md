# FitLog

Trainingslogbuch als Python-Konsolenanwendung.

## Starten

Im Projektordner ausführen:

```bash
python main.py
```

Unter Windows geht auch `py main.py`, unter Linux/macOS `python3 main.py`.
Python 3 und die Standardbibliothek reichen aus.

Beim ersten Start entsteht `data/fitlog.json` mit sechs Übungen,
einer leeren Trainingsliste und dem Wochenziel 3. Weitere Starts laden
wieder dieselbe Datei. Beschädigte Daten werden mit einer Meldung
abgelehnt und nicht überschrieben.

## Stand vom 15. November 2026

| Menüpunkt | Funktion | Stand |
| --- | --- | --- |
| 0 | Beenden | Vorhanden |
| 1 | Übungen anzeigen | Vorhanden |
| 2 | Übung hinzufügen | Vorhanden, wird sofort gespeichert |
| 3 | Übungen suchen | Vorhanden |
| 4 | Training erfassen | Vorhanden, wird sofort gespeichert |
| 5 | Training löschen | Vorhanden, mit Bestätigung und sofortigem Speichern |
| 6 | Historie und Übungsfilter | Vorhanden |
| 7 | Erstes, letztes und bestes Gewicht | Vorhanden |
| 8 | Volumen pro Muskelgruppe | Vorhanden |
| 9 | Wochenziel und Serie | Vorhanden, Änderungen werden sofort gespeichert |
| 10 | Wochenbericht als CSV | Vorhanden |

Alle Menüpunkte sind angeschlossen. Hinzufügen, Erfassen und Löschen
werden sofort gespeichert. Bei Schreibfehlern wird die Änderung
im Arbeitsspeicher zurückgenommen; die bisherige Datei bleibt erhalten.
Der aktuelle Teststand steht in [docs/testprotokoll.md](docs/testprotokoll.md).

Alle Auswertungen arbeiten mit demselben geladenen Datenbestand.
Neue Übungen stehen direkt bei der Trainingserfassung zur Auswahl.
Sie verändern die Reihenfolge der gespeicherten Trainings nicht.
Bei gleichem Datum bleibt die Erfassungsreihenfolge erhalten.
Für den Fortschritt sind mindestens zwei Einträge derselben Übung nötig.
Volumen bedeutet Sätze × Wiederholungen × Gewicht; 0 kg ergeben Volumen 0.

Das Wochenziel zählt verschiedene Trainingstage von Montag bis Sonntag.
Die Serie berücksichtigt abgeschlossene Wochen ab der Vorwoche.
Eine Zieländerung gilt auch für die Berechnung der bisherigen Serie.

CSV-Dateien liegen unter `reports/weekly_report_YYYY_CWxx.csv`.
Der Export enthält die aktuelle Woche, Semikolon als Trennzeichen und
UTF-8 mit BOM für Excel. Ein erneuter Export ersetzt den Wochenbericht.

## Tests

```bash
python -m unittest discover -s tests -v
```

68 Tests prüfen die Fachfunktionen und den Gesamtablauf.
Die Tests verwenden erfundene Daten und für Dateizugriffe temporäre Ordner.
Die Menüfunktion `main(data)` kann für Tests auch einen Bestand entgegennehmen.
Ohne Parameter lädt sie die JSON-Datei.

## Beispieldaten ausprobieren

Auf einem frischen Teststand zuerst mit `0` beenden. Danach kann die Datei
`examples/fitlog.sample.json` nach `data/fitlog.json` kopiert werden.
Vorhandene persönliche Daten vorher separat sichern. Die Beispieldaten
werden nicht automatisch importiert und enthalten ältere Trainingsdaten.
Ein Export kann daher für die aktuelle Woche nur die Kopfzeile enthalten.

## Zuständigkeiten

| Person | Eigener Bereich |
| --- | --- |
| Rudina | US1 bis US3: Übungen |
| Sema | US4 bis US6: Trainings und Eingabeprüfung |
| Raul | US7 bis US9: Statistik; Menüintegration und Koordination |
| Patrick | US10 bis US12: Speicherung, Wochenziel und Export |

Die Aufgaben und Akzeptanzkriterien stehen in den GitHub-Issues.
Jede Person prüft und erklärt ihren eigenen Beitrag. Änderungen an
geteilten Dateien werden über Branches und Pull Requests abgestimmt.
Die Feldnamen und Regeln stehen in [docs/datenmodell.md](docs/datenmodell.md).
Persönliche Daten unter `data/` und Berichte unter `reports/` sind nicht versioniert.
