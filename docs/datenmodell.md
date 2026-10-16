# Gemeinsame Datenstruktur für FitLog

Status: konkreter Vorschlag zur gemeinsamen Prüfung im Pull Request.
Die aktuelle Datei „FitLog - User Stories.docx“ ist die fachliche Grundlage.
Die unten genannten zusätzlichen Detailentscheidungen sind Vorschläge;
eine Zustimmung des Teams wird damit nicht behauptet.

## Überblick

Patrick speichert den gesamten Bestand in `data/fitlog.json`.
Im laufenden Python-Programm wird dieselbe Struktur als Dictionary mit
Listen und weiteren Dictionaries verwendet. Jedes Training verweist
über `exercise_id` auf eine Übung.

| Feld im Gesamtbestand | JSON-Typ | Bedeutung |
| --- | --- | --- |
| `format` | string | Feste Formatkennung `fitlog-v1` |
| `exercises` | array | Liste der Übungen |
| `workouts` | array | Liste der Trainingseinträge in Erfassungsreihenfolge |
| `weekly_goal` | integer | Wochenziel von 1 bis 7 Trainingstagen, Vorgabe 3 |

Ein vollständiges Beispiel mit erfundenen Daten steht in
[examples/fitlog.sample.json](../examples/fitlog.sample.json).
Es wird nicht automatisch als persönlicher Datenbestand geladen.

## Übung

| Feld | JSON-Typ | Regel | Verwendet von |
| --- | --- | --- | --- |
| `id` | string | Nicht leer, innerhalb der Übungen eindeutig und dauerhaft stabil | Alle Bereiche |
| `name` | string | Nach Bereinigung 1 bis 60 Zeichen; Namen ohne Beachtung der Gross-/Kleinschreibung eindeutig | Rudina; Anzeige und Export |
| `muscle_group` | string | Genau einer der sechs Werte unten | Rudina; Raul US9; Patrick US12 |

Zulässige Muskelgruppen: `Chest`, `Back`, `Legs`, `Shoulders`,
`Arms`, `Core`. Jede Übung gehört genau einer Hauptmuskelgruppe an.

Führende und folgende Leerzeichen im Namen werden entfernt;
mehrere aufeinanderfolgende Leerzeichen werden zu einem.
Die ID wird beim Anlegen einmal erzeugt, beispielsweise mit
`uuid.uuid4().hex`. Sie hängt nicht von der sichtbaren Auswahlposition ab.
Die kurzen IDs der Beispieldatei dienen nur der Lesbarkeit.

Beim ersten Start werden sechs Übungen angelegt, eine pro Muskelgruppe.
Vorgeschlagene Namen stehen in der Beispieldatei. Der konkrete
Startkatalog ist eine gemeinsame Detailentscheidung.

## Trainingseintrag

| Feld | JSON-Typ | Regel | Verwendet von |
| --- | --- | --- | --- |
| `id` | string | Nicht leer, innerhalb der Einträge eindeutig und dauerhaft stabil | Sema US6 |
| `exercise_id` | string | Verweist auf eine vorhandene Übung | Sema; Raul; Patrick |
| `date` | string | Gültiges Kalenderdatum als `YYYY-MM-DD` | Historie; Fortschritt; Woche |
| `sets` | integer | 1 bis 20 | Volumenberechnung |
| `reps` | integer | 1 bis 100; Wiederholungen pro Satz | Volumenberechnung |
| `weight` | number | Endliche Zahl ab 0, in kg; 0 für Körpergewichtsübungen | Fortschritt und Volumen |

Ein Trainingseintrag beschreibt eine Übung mit einer Anzahl gleichartiger
Sätze an einem Datum. Drei Sätze sind ein Eintrag, kein einzelner Eintrag
pro Satz. Unterschiedliche Gewichte können als getrennte Einträge
erfasst werden. Neue Einträge werden an die Liste angehängt.

Leere Datumseingabe bedeutet heute; gespeichert wird das konkrete Datum.
Ein Punkt oder Komma kann bei der Eingabe des Gewichts akzeptiert werden.
In JSON steht das Gewicht als Zahl mit einem Punkt als Dezimaltrenner.
`NaN`, Unendlich und negative Gewichte sind ungültig.

Übungsname und Muskelgruppe werden über `exercise_id` nachgeschlagen.
Sie werden nicht zusätzlich im Training gespeichert.
Die sichtbare Nummer in einem Menü ist nur eine Auswahlhilfe.
Beim Löschen wird diese Auswahl auf die stabile ID abgebildet.

## Berechnete Werte

Volumen, Fortschritt, Wochenbericht und Serie werden aus dem Bestand
berechnet und nicht als zweite Kopie dauerhaft gespeichert.

- US7: Historie nach Datum aufsteigend anzeigen; nach Übung optional filtern.
  Für die Anzeige eine sortierte Kopie verwenden; Speicherreihenfolge erhalten.
- US8: Nur die ausgewählte Übung auswerten. Bestes Gewicht ist das Maximum;
  erstes und letztes Gewicht stammen aus der chronologisch sortierten
  Folge. Fortschritt ist letztes minus erstes Gewicht, mit Vorzeichen.
  Bei weniger als zwei Einträgen die vorgegebene Meldung anzeigen.
- US9: Pro Eintrag `sets * reps * weight` rechnen und nach Muskelgruppe
  summieren; absteigend anzeigen. Gewicht 0 ergibt Volumen 0.
- US11: Mehrere Einträge am gleichen Datum zählen zusammen als ein
  Trainingstag. Eine Woche läuft Montag bis Sonntag.
- US12: Den aktuellen Wochenbericht aus den Einträgen ableiten.

## Zusätzliche Detailentscheidungen zur Prüfung

1. Bei gleichem Datum bleibt für US8 die Erfassungsreihenfolge erhalten.
   Der erste und letzte Eintrag sind damit auch bei mehreren Einträgen
   an einem Tag eindeutig. Es wird kein Tagesmaximum als Ersatz für
   den ersten oder letzten Eintrag verwendet.
2. `weekly_goal` ist eine globale Zielzahl, wie in den aktuellen Stories
   beschrieben. Vorschlag: Die Serie prüft abgeschlossene Wochen
   rückwärts ab der letzten Woche gegen diesen aktuellen Zielwert;
   bei der ersten verfehlten Woche endet die Serie. Eine Zieländerung
   wirkt dadurch auch auf die angezeigte historische Serie.
   Diese Wirkung vor der Umsetzung von US11 gemeinsam bestätigen.
3. Das Handbuch zeigt teilweise `muscle` und historische
   `weekly_goals`. Dieser Vorschlag verwendet einheitlich
   `muscle_group` und `weekly_goal`. Bei einer späteren Entscheidung
   für historische Ziele müssen Format und US11 gemeinsam angepasst werden.
4. Für US8 gelten die aktuellen Word-Kriterien: bestes, erstes und letztes
   Gewicht. Die abweichende Tagesvergleichslogik im Handbuch ist
   keine zusätzliche Anforderung.

## Speichern und Laden

Verantwortlich: Patrick, US10.

- Dateipfad: `data/fitlog.json`; Textkodierung UTF-8.
- Beim echten ersten Start: sechs Startübungen, leere Trainingsliste,
  Ziel 3 und Formatkennung erzeugen und speichern.
- Beim Laden Top-Level-Felder, Datentypen, Wertebereiche,
  Eindeutigkeit der IDs, Übungsreferenzen, bereinigte eindeutige Namen
  und die sechs zulässigen Muskelgruppen prüfen.
- Fehlerhafte vorhandene Dateien nicht überschreiben oder durch
  leere Daten ersetzen. Fehlermeldung ausgeben und Programm stoppen.
- Änderungen erst vollständig prüfen und unmittelbar speichern.
  Bei Schreibfehlern bleibt die bisherige gespeicherte Datei erhalten.
  Vorschlag: neue Datei im gleichen Ordner temporär schreiben
  und die Zieldatei erst nach erfolgreichem Schreiben atomar ersetzen.
- Bei einem fehlgeschlagenen Speichervorgang keine erfolgreiche Änderung
  bestätigen; den bisherigen Stand im Arbeitsspeicher beibehalten.
- Beim Schreiben echte Umlaute erhalten und nicht endliche Zahlen ablehnen,
  beispielsweise mit `ensure_ascii=False` und `allow_nan=False`.

## CSV-Export

Verantwortlich: Patrick, US12.

Pfad: `reports/weekly_report_YYYY_CWxx.csv`.
Für Jahreszahl und Kalenderwoche die zusammengehörigen ISO-Wochenwerte
verwenden, damit der Jahreswechsel korrekt ist.

Spalten in dieser Reihenfolge:

`date;exercise;muscle_group;sets;reps;weight;volume`

Eine Zeile pro Trainingseintrag der laufenden Woche.
`exercise` und `muscle_group` über die Übungsreferenz auflösen;
`volume` beim Export berechnen.
UTF-8 mit BOM ist als Vorschlag für Excel vorgesehen.
Textfelder mit führendem `=`, `+`, `-` oder `@` durch ein
vorangestelltes Apostroph entschärfen. Diese Exportdarstellung
verändert die gespeicherten Trainingsdaten nicht.

## Zusammenarbeit an den Schnittstellen

| Person | Eigener Bereich | Gemeinsame Abstimmung |
| --- | --- | --- |
| Rudina | `exercises`: anzeigen, ergänzen, suchen | IDs und Muskelgruppen mit Sema, Raul und Patrick |
| Sema | `workouts`: erfassen, prüfen, löschen | Übungsreferenzen und Speichern mit Rudina und Patrick |
| Raul | Historie, Fortschritt, Gruppenvolumen | Unveränderte Speicherreihenfolge; lesender Zugriff auf Übungen und Trainings |
| Patrick | Laden/Speichern, Ziel, Export | Formatprüfung und Speicherfehler mit allen Bereichen |

Als einfache gemeinsame Funktionsgrenze kann Patrick
`load_data() -> dict` und `save_data(data) -> None` bereitstellen.
Fachfunktionen erhalten den Bestand bzw. die benötigten Listen als
Parameter; sie lesen nicht jeweils eigene Dateikopien ein.
Die konkreten Funktionsnamen stimmt das Team vor der Implementierung ab.

Die zwölf Aufgaben sind in [user_stories.md](user_stories.md) verlinkt.
