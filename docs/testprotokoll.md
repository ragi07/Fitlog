# Teststand vom 23. November 2026

## Wiederholbare Tests

Im Projektordner:

```bash
python -m unittest discover -s tests -v
```

Ergebnis: 68 Tests bestanden.

| Bereich | Geprüft |
| --- | --- |
| Übungen | Hinzufügen über Menü, eindeutige ID und sofortiges Speichern |
| Suche | Geladener Katalog, Teilwort und unveränderte gespeicherte Daten |
| Erfassung | Numerische IDs, Auswahl, Felder, Fehleingaben und genau ein gespeicherter Eintrag |
| Löschen | Bestätigung, Abbruch, Erhalt anderer Trainings und sofortiges Speichern |
| Historie | Sortierung, Filter, gleiche Tage, leere Ergebnisse und unveränderte Reihenfolge |
| Fortschritt | Erstes, letztes und bestes Gewicht, Vorzeichen und zu wenige Einträge |
| Volumen | Handrechnung, Gruppensummen, Sortierung, Dezimalgewichte und 0 kg |
| Erststart/Neustart | Sechs Übungen, leere Trainings, Wochenziel 3; Daten über Neustarts erhalten |
| Dateifehler | Beschädigte Datei bleibt erhalten, Lesefehler werden gemeldet |
| Schreibfehler | Hinzufügen, Erfassen, Löschen und Zieländerung werden zurückgenommen |
| Wochenziel | Bestätigung, Abbruch und sofortiges Speichern |
| Export | Geladene Trainings, gleiche Tage, leere Woche und Schreibfehler |

## Vollständiger Konsolenablauf

Ein Test startet das tatsächliche Programm in einem eigenen Prozess:

1. Neue Übung hinzufügen und suchen.
2. Zwei Trainings für diese Übung erfassen.
3. Historie, Fortschritt und Gruppenvolumen anzeigen.
4. Wochenziel ändern und Wochenbericht exportieren.
5. Einen Eintrag löschen und den Bericht erneut exportieren.
6. Beenden und in einem neuen Prozess starten.
7. Verbleibenden Eintrag, Fortschrittsmeldung, Volumen, Wochenziel und Export prüfen.

Handrechnung im Test: 3 × 10 × 50 + 2 × 8 × 55 = 2380.
Nach Löschen des ersten Trainings verbleiben 880.
Fortschritt vor dem Löschen: 55 − 50 = +5 kg.

Ein weiterer Test löscht das letzte Training und prüft danach die leere
Historie, Fortschritt, Volumen, 0 Trainingstage und einen Bericht mit nur
Kopfzeile. Bei einem Löschabbruch bleibt die Datei bytegleich.
Alle Dateitests laufen in temporären Ordnern.

## Zusätzlich gezielt geprüfte Bausteine

- US2: ID-Lücken, leere/zu lange/doppelte Namen, Bereinigung und erneute Muskelgruppenwahl.
- US3: leere Suche, Teilwort, Gross-/Kleinschreibung, Muskelgruppe und keine Treffer.
- US4/US6: numerische und unsortierte IDs, neue ID nach Löschen und Erhalt anderer Einträge.
- US5: 15 Eingabefälle, darunter negative Gewichte, Komma/Punkt, falsche Daten und y/n.
- US10: gültiger Bestand und 18 ungültige Varianten; beschädigte Datei;
  Dateierhalt bei Schreib- und Ersetzfehlern.
- US11: Wochen- und Jahreswechsel, doppelte Trainingstage und Serie ohne aktuelle Woche.
- US12: ISO-Woche am Jahreswechsel, Umlaute/BOM, Formelschutz und Ersetzen des Berichts.

## Nachtrag US4 abgeschlossen

Semas PR #31 korrigiert die Übungsreferenz in `manual_test_us4.py` von
`"ex-bench"` auf `1`. Die Änderung wurde geprüft und am 23. November übernommen.
Der Testnachweis mit numerischen IDs steht in Issue #29 und PR #31.

Der korrigierte Test wurde zusätzlich mit vorgegebenen Terminaleingaben ausgeführt:
ungültiges Datum, falsche Übungsauswahl, ungültige Sätze und Wiederholungen sowie
negatives Gewicht werden abgelehnt. Anschliessend entsteht genau ein neuer Eintrag
mit ID 2 und Übungs-ID 3. Die ID-Fälle 3/1/2, 3/1 und leere Liste liefern 4, 4 und 1.
Alle 68 automatischen Tests bestehen am 23. November erneut.

## Noch gemeinsam prüfen

- Start anhand der README auf einem zweiten Rechner durchführen und Ergebnis festhalten.
- Jede Person erklärt ihre drei User Stories und die verwendeten Daten.
- Den Menüablauf für die Präsentation gemeinsam durchspielen.

Eine kleine Unstimmigkeit bleibt bei der Ausgabe: `workouts.py` meldet
„Workout saved“ bereits vor dem Dateischreiben in `main.py`. Bei einem
Schreibfehler folgen Fehlermeldung und Rücknahme korrekt; die vorzeitige
Erfolgsmeldung sollte noch angepasst werden.
