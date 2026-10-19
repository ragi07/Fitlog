# FitLog

Python Trainingslogbuch im Modul Grundlagen Programmieren.

## Aktueller Stand

Dieser Branch bereitet das Hauptmenue vor. Die Optionen 1 bis 10 zeigen
ausdrücklich Platzhalter; mit 0 wird das Programm beendet.
Es werden noch keine Trainingsdaten verarbeitet oder gespeichert.

## Starten

Voraussetzung: Python 3.6 oder neuer; keine zusätzlichen Pakete erforderlich.
Im Projektordner ausführen:

```bash
python main.py
```

Unter Windows kann alternativ `py main.py` verwendet werden.

## Zuständigkeiten nach den aktuellen User Stories

| Person | User Stories | Bereich |
| --- | --- | --- |
| Rudina | US1 bis US3 | Übungen anzeigen, hinzufügen und suchen |
| Sema | US4 bis US6 | Training erfassen, Eingaben prüfen und Einträge löschen |
| Raul | US7 bis US9 | Historie, Fortschritt und Volumen pro Muskelgruppe |
| Patrick | US10 bis US12 | JSON, Wochenziel und CSV-Export |

Raul bereitet zusätzlich die Menüintegration vor.
Das alte Excel ist keine Grundlage für diese Zuordnung.

## Zusammenarbeit

1. Vor einer neuen Aufgabe den lokalen main aktualisieren.
2. Einen Branch für eine zusammenhängende Aufgabe erstellen.
3. Eigene Änderungen entwickeln, prüfen und committen.
4. Den Branch zu GitHub pushen und einen Pull Request nach main öffnen.
5. Nach dem Review zusammenführen und den lokalen main aktualisieren.

Änderungen an gemeinsamen Dateien vorher absprechen.
Jede Person committet ihre eigenen Änderungen.
Lokale Trainingsdaten in data/ und erzeugte Berichte in reports/
werden nicht versioniert.
