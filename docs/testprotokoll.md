# Teststand vom 9. November 2026

## Wiederholbare Tests

Im Projektordner:

```bash
python -m unittest discover -s tests -v
```

Ergebnis: 56 Tests bestanden.

| Bereich | Geprüft |
| --- | --- |
| Historie | Sortierung, Filter, gleiche Tage, leere Ergebnisse und unveränderte Daten |
| Fortschritt | Erstes, letztes und bestes Gewicht, Vorzeichen, gleiche Tage und zu wenige Einträge |
| Volumen | Handrechnung, Gruppensummen, Sortierung, Dezimalgewichte und 0 kg |
| Menü | Statistikaufrufe, ungültige Menüauswahl und Beenden |
| Erststart/Neustart | Datei wird angelegt, gespeicherte Übungen und Trainings werden geladen |
| Dateifehler | Kaputte Datei bleibt erhalten, Lesefehler werden gemeldet |
| Wochenziel | Bestätigung, Abbruch, sofortiges Speichern und Rücknahme bei Speicherfehler |
| Export | Aufruf über Menü, geladene Trainings, gleiche Tage, leere Woche und Schreibfehler |

Zwei Prüfungen starten das tatsächliche Programm in separaten Prozessen.
Eine davon prüft den Neustart mit gespeicherten Trainings; die andere
prüft das kontrollierte Stoppen bei ungültiger Datei.
Alle Dateitests laufen in temporären Ordnern.

## Zusätzlich gezielt geprüfte Bausteine

- US5: 15 Eingabefälle, darunter negative Gewichte, Komma/Punkt, falsche Daten und y/n.
- US10: gültiger Bestand und 18 ungültige Varianten; Erststart und Neustart;
  beschädigte JSON-Datei; Erhalt der alten Datei bei Schreib- und Ersetzfehlern.
- US11: Wochen- und Jahreswechsel, doppelte Trainingstage und Serie ohne aktuelle Woche.
- US12: ISO-Woche am Jahreswechsel, Wochenfilter, Umlaute/BOM,
  Formelschutz, berechnetes Volumen und Ersetzen eines vorhandenen Berichts.

## Noch offen

Der Gesamtablauf mit Übung hinzufügen, Training erfassen und Löschen ist
noch nicht abgenommen. Diese Funktionen sind noch nicht auf main angeschlossen.

| Beitrag | Ergebnis der Prüfung | Nächster Schritt |
| --- | --- | --- |
| US2, PR #22 | Mit IDs 1 und 3 entsteht erneut ID 3 | Rudina korrigiert die ID-Vergabe und wiederholt ungültige Namen |
| US3 | Geprüfte Suchfälle funktionieren auf Rudinas Branch | Rudina eröffnet einen PR mit dem aktuellen main-Stand |
| US4, PR #24 | Numerische Trainings-ID führt zum Fehler; neue ID ist noch Text | Sema stellt Code und Tests auf numerische IDs um |
| US6, PR #25 | Löschfunktion besteht die geprüften Fälle | Sema übernimmt die ID-Korrektur aus US4 und aktualisiert die Testdaten |

Nach den Korrekturen: Beiträge erneut reviewen, in der Reihenfolge
US2/US3 sowie US4 vor US6 übernehmen und die Menüpunkte anschliessen.
Dann den vollständigen Ablauf mit Neustart und allen Auswertungen testen.
Ein bestandener Bausteintest ersetzt diese gemeinsame Abnahme nicht.
