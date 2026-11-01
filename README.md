# FitLog

Python Trainingslogbuch im Modul Grundlagen Programmieren.

## Starten

Python 3 im Projektordner ausführen:

```bash
python main.py
```

Unter Windows funktioniert alternativ `py main.py`.

## Aktueller Stand

Menüpunkt 1 zeigt die Übungen. Menüpunkt 6 zeigt die Trainingshistorie
und bietet einen Filter für eine einzelne Übung oder alle Übungen.
Menüpunkt 7 vergleicht das erste, letzte und höchste Gewicht einer Übung
und zeigt die Veränderung mit Vorzeichen. Zwei Einträge sind notwendig.
Mehrere Einträge am gleichen Tag bleiben in ihrer Erfassungsreihenfolge.
Die übrigen Fachfunktionen sind noch Platzhalter.

Die Statistik verwendet den gemeinsamen Datenbestand mit den Feldern
`exercises`, `workouts` und `weekly_goal`. Das Menü nimmt diesen Bestand
als Parameter entgegen: `main(data)`. Ohne übergebene Daten startet es
mit sechs Übungen und ohne Trainings. Sobald US10 bereit ist, wird
beim Start der Rückgabewert von `load_data()` übergeben. Dieser Anschluss
ist noch offen. Die Statistik selbst verändert und speichert keine Daten.

## Tests

```bash
python -m unittest discover -s tests -v
```

Die Tests prüfen die fachlichen Ergebnisse und den Menüablauf mit
vorgegebenen Eingaben. Sie verwenden erfundene Trainingsdaten.

## Zuständigkeiten

| Person | User Stories | Bereich |
| --- | --- | --- |
| Rudina | US1 bis US3 | Übungen anzeigen, hinzufügen und suchen |
| Sema | US4 bis US6 | Training erfassen, Eingaben prüfen und Einträge löschen |
| Raul | US7 bis US9 | Historie, Fortschritt und Volumen pro Muskelgruppe |
| Patrick | US10 bis US12 | JSON, Wochenziel und CSV-Export |

Raul bereitet zusätzlich die Menüintegration vor. Vor Änderungen an
geteilten Dateien die betroffenen Funktionen miteinander absprechen.
Jede Person committet ihre eigenen Änderungen. Änderungen werden
über einen Branch und einen Pull Request gemeinsam geprüft.

Das Datenmodell steht in [docs/datenmodell.md](docs/datenmodell.md),
die Aufgaben in [docs/user_stories.md](docs/user_stories.md).
Übungs- und Trainings-IDs sind positive ganze Zahlen.
Persönliche Trainingsdaten unter `data/` und erzeugte Berichte unter
`reports/` werden nicht versioniert.
