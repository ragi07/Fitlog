# FitLog

**Trainings erfassen, Fortschritte vergleichen und die Trainingswoche auswerten.**

FitLog ist unsere Python-Konsolenanwendung für das Modul Grundlagen Programmierung.
Übungen und Trainings werden lokal gespeichert und bleiben nach einem Neustart erhalten.

**Team:** Rudina, Sema, Raul und Patrick.

## Starten

Python 3 genügt. Es müssen keine zusätzlichen Pakete installiert werden.

1. Repository herunterladen oder klonen.
2. Terminal im Projektordner öffnen.
3. Programm starten:

```bash
python main.py
```

Unter Windows funktioniert auch `py main.py`, unter Linux/macOS `python3 main.py`.
Das Menü bietet die Optionen 1 bis 10; mit `0` wird das Programm beendet.

Beim ersten Start legt FitLog sechs Standardübungen, eine leere Trainingsliste
und das Wochenziel 3 an. Die Daten liegen in `data/fitlog.json`.

## User Stories und Umsetzung

Alle zwölf User Stories sind umgesetzt und im Hauptmenü verbunden.
Jede Person hat drei User Stories übernommen.

| Person | User Story | Menü | Inhalt |
| --- | --- | --- | --- |
| Rudina | [US1: Übungen anzeigen](https://github.com/ragi07/Fitlog/issues/2) | 1 | Übungen nach Muskelgruppe und Name sortieren; sechs Standardübungen beim Erststart. |
| Rudina | [US2: Übung hinzufügen](https://github.com/ragi07/Fitlog/issues/3) | 2 | Namen bereinigen, Duplikate verhindern, Muskelgruppe wählen und eine eindeutige ID vergeben. |
| Rudina | [US3: Übungen suchen](https://github.com/ragi07/Fitlog/issues/4) | 3 | Namen und Muskelgruppen durchsuchen, auch mit Teilwörtern und unabhängig von Gross-/Kleinschreibung. |
| Sema | [US4: Training erfassen](https://github.com/ragi07/Fitlog/issues/5) | 4 | Datum, Übung, Sätze, Wiederholungen und Gewicht erfassen; den Eintrag nach gültiger Eingabe anlegen. |
| Sema | [US5: Eingaben prüfen](https://github.com/ragi07/Fitlog/issues/6) | Übergreifend | Menüwahl, Zahlen, Datum und y/n prüfen; nur die fehlerhafte Eingabe erneut abfragen. |
| Sema | [US6: Training löschen](https://github.com/ragi07/Fitlog/issues/7) | 5 | Ein Training auswählen und nach Bestätigung löschen; andere Einträge und Übungen bleiben erhalten. |
| Raul | [US7: Trainingshistorie](https://github.com/ragi07/Fitlog/issues/8) | 6 | Trainings chronologisch anzeigen und nach einer Übung filtern. |
| Raul | [US8: Fortschritt](https://github.com/ragi07/Fitlog/issues/9) | 7 | Erstes, letztes und bestes Gewicht einer Übung sowie die Veränderung in kg anzeigen. |
| Raul | [US9: Trainingsvolumen](https://github.com/ragi07/Fitlog/issues/10) | 8 | Volumen je Muskelgruppe berechnen und absteigend anzeigen. |
| Patrick | [US10: Daten speichern und laden](https://github.com/ragi07/Fitlog/issues/11) | Übergreifend | JSON-Datei laden und prüfen, Änderungen speichern und beschädigte Dateien vor Überschreiben schützen. |
| Patrick | [US11: Wochenziel und Serie](https://github.com/ragi07/Fitlog/issues/12) | 9 | Trainingstage zählen, Wochenziel ändern und die Serie erreichter Wochen anzeigen. |
| Patrick | [US12: Wochenbericht](https://github.com/ragi07/Fitlog/issues/13) | 10 | Trainings der aktuellen Woche als CSV für Excel exportieren, inklusive Volumen und Zielauswertung. |

Raul übernimmt zusätzlich die Koordination und die gemeinsame Menüintegration.
Die Beiträge wurden über Branches, Pull Requests und Reviews zusammengeführt.
Die vollständigen Akzeptanzkriterien stehen in den verlinkten Issues.

## Beispielablauf für die Vorstellung

1. Eine neue Übung anlegen und über die Suche finden.
2. Zwei Trainings derselben Übung erfassen, dabei einmal absichtlich eine falsche Eingabe machen.
3. Historie, Fortschritt und Volumen anzeigen.
4. Wochenziel ansehen und einen CSV-Bericht exportieren.
5. Ein Training mit Bestätigung löschen.
6. FitLog beenden und neu starten: Die verbleibenden Daten sind weiterhin vorhanden.

**Rechenbeispiel:** 3 Sätze × 10 Wiederholungen × 50 kg ergeben ein Volumen von 1500.
Steigt das Gewicht beim nächsten Training von 50 auf 55 kg, zeigt der Fortschritt **+5 kg**.

## Regeln der Auswertung

- Fortschritt benötigt mindestens zwei Einträge derselben Übung. Bei gleichem Datum gilt die Erfassungsreihenfolge.
- Volumen ist Sätze × Wiederholungen × Gewicht. Körpergewichtsübungen mit 0 kg ergeben Volumen 0.
- Das Wochenziel zählt verschiedene Trainingstage von Montag bis Sonntag.
- Die Serie berücksichtigt abgeschlossene Wochen ab der Vorwoche. Eine Zieländerung wirkt auch auf die bisherige Serie.
- Der CSV-Bericht enthält die aktuelle Woche. Ein erneuter Export ersetzt den Bericht derselben Woche.

## Aufbau und Daten

| Datei | Aufgabe |
| --- | --- |
| `main.py` | Hauptmenü und Verbindung der Funktionen mit dem gemeinsamen Datenbestand |
| `exercises.py` | Übungskatalog, Hinzufügen und Suche |
| `workouts.py`, `validation.py` | Trainingseinträge und gemeinsame Eingabeprüfung |
| `analytics.py` | Historie, Fortschritt und Gruppenvolumen |
| `storage.py` | JSON-Datei, Datenprüfung und ID-Vergabe |
| `goals.py`, `report.py` | Wochenziel, Serie und CSV-Export |

Hinzufügen, Erfassen, Löschen und Zieländerungen werden sofort gespeichert.
Schlägt das Schreiben fehl, wird die Änderung zurückgenommen; die bisherige Datei bleibt erhalten.
Beschädigte vorhandene Daten werden beim Start mit einer Fehlermeldung abgelehnt.

Berichte liegen unter `reports/weekly_report_YYYY_CWxx.csv`.
Sie verwenden Semikolon und UTF-8 mit BOM für Excel.
Persönliche Daten und erzeugte Berichte werden nicht ins Repository übernommen.

## Tests

```bash
python -m unittest discover -s tests -v
```

**Stand 23. November 2026: 68 automatische Tests bestanden.**
Geprüft werden unter anderem Berechnungen, Fehleingaben, Speicherfehler und
der vollständige Menüablauf mit einem echten Programmneustart.
Dateitests verwenden temporäre Ordner und erfundene Daten.

Die zusätzlichen Testdateien `manual_test_us4.py`, `manual_test_us5.py`
und `manual_test_us6.py` lassen sich einzeln starten und erwarten Eingaben im Terminal.
Details und noch ausstehende Teamprüfungen stehen im [Testprotokoll](docs/testprotokoll.md).

## Beispieldaten und Dokumentation

Für einen Test mit Beispieldaten FitLog zuerst starten und mit `0` beenden.
Danach `examples/fitlog.sample.json` nach `data/fitlog.json` kopieren.
Eigene Daten vorher sichern. Die Beispieldatei enthält ältere Trainings;
für einen gefüllten aktuellen Wochenbericht neue Trainings mit heutigem Datum erfassen.

- [Datenmodell](docs/datenmodell.md)
- [User Stories und Zuständigkeiten](docs/user_stories.md)
- [Testprotokoll](docs/testprotokoll.md)
