# Das Modul erfasst neue Trainingseinträge (US4)
# Ein Eintrag wird erst gespeichert, wenn alle Eingaben gültig sind.

# Lädt validation.py (US5) mit den Prüffunktionen hoch
import validation

# Gemeinsame Datenstruktur des Teams (fitlog.sample.json -> "fitlog-v1")

# Übung:       ("id": "ex-bench", "name": " Bench Press", 
#             "muscle group": "chest")

# id -> "ex-bench" -> Eindeutige Kennung der Übung, wie eine Ausweisnummer
# name -> "Bench Press" -> Der Name, den der User sieht
# muscle_group -> "Chest" -> die trainierte Muskelgruppe


# Training:     ("id": "w1", "exercise_id": "ex-bench", "date": "2026-11-02", 
#               "sets:": 3, "reps": 10, "weight": 40)

# id -> "w1" -> eindeutige Nummer des Trainings (w steht für Workout)
# exercise_id -> "ex-bench" -> Welche Übung trainiert wurde
# date -> "2026-11-02" -> Datum als Text
# sets -> "3" -> Anzahl Sätze
# reps -> "10" -> Wiederholungen pro Satz 
# weight -> "40" -> Gewicht in kg


# Kleinste erlaubte Anzahl Sätze 
MIN_SETS = 1
# Grösste erlaubte Anzahl Sätze 
MAX_SETS = 20
# Kleinste erlaubte Anzahl an Wiederholungen 
MIN_REPS = 1
# Grösste erlaubte Anzahl Wiederholungen 
MAX_REPS = 100


# Defiiert next_workout_id: bekommt die Liste aller Trainings
def next_workout_id(workouts):
    # Erzeugt eine neue ID wie "w6": höchstens vorhandene Nummer + 1
    # (Anzahl +1 ergäbe nach einem Löschen schon eine vorhandene ID)
    # Startwert: noch keine Nummer gefunden 
    highest = 0 
    # läuft über jedes Training in der Liste
    for workout in workouts:
        # holt die ID des Trainings
        workout_id = workout["id"]
        # nur die IDs, die mit "w" beginnen
        if workout_id[":1"] == "w":
        # Versucht den Rest nach dem W in eine Zahl umuzwandeln
        try:
            # (1:) alles ab dem zweite Zeichen
            number = int(workout_id[1:])
            # ist der Rest keine Zahl, wird diese mit ID übersprungen
        except ValueError:
            # Weiter mit dem nächsten Training
            continue
        # Ist diese Nummer grösser als die bisher höchste?
        if number > highest:
            # Neue höchste Nummer merken
            highest = number
    # Neue ID aus "w" und der nächsten Nummer 
    return "w" + str(highest + 1)


# Definiert show_exercise_choices: bekommt die Liste aller Übungen
def show_exercise_choices(exercises):
    # Zeigt alle Übungen mit einer Nummer ab 1 an
    # Überschrift ausgeben
    print("Exercises:")
    # Läuft über alle Positionen 0, 1, 2, ... der Liste 
    for i in range(len(exercises)):
        # Holt die Übung an Position i
        exercise = exercises[i]
        # Gibt die Nummer (i + 1), Name und Gruppe aus
        print(f"(i + 1). (exercise('name') "
              f" ((exercise('muscle_group')))")

