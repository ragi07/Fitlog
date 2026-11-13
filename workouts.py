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


# Training:     ("id": "1", "exercise_id": "ex-bench", "date": "2026-11-02", 
#               "sets:": 3, "reps": 10, "weight": 40)

# id -> "1" -> eindeutige Nummer des Trainings (w steht für Workout)
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
    # Erzeugt eine neue ID wie "6": höchstens vorhandene Nummer + 1
    # (Anzahl +1 ergäbe nach einem Löschen schon eine vorhandene ID)
    # Startwert: noch keine Nummer gefunden 
    highest = 0 
    # läuft über jedes Training in der Liste
    for workout in workouts:
        # holt die ID des Trainings
        if workout["id"] > highest:
            # Neue höchste ID merken
            highest = workout["id"]
    # Gibt die nächste freie Zahl zurück, z.B. 3 + 1 = 4
    return highest + 1


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
        print(f"{i + 1}. {exercise['name']} "
              f" ({exercise['muscle_group']})")


# Definiert log_workout: bekommt Übungsliste und Trainingsliste
def log_workout(exercises, workouts):
    # US4: Fragt alle Werte ab und hängt EINEN gültigen Eintrag an
    # Gibt den neuen Eintrag zurück (oder None, wenn es keine Übung gibt)
    # Gibt es noch keine Übung? Länge der Liste ist 0
    if len(exercises) == 0:
        # Hinweis laut US4: zuerst eine Übung hinzufügen
        print("No exercises available. " 
        "Please add an exercise first (menu option 2).")
        # Funktion beenden, nichts gespeichert. None = "Kein Ergebnis"
        return None
    
    # Fragt das Datum ab (validation.py prüft es): leer = heute
    date = validation.read_date("Date (YYYY-MM-DD, empty = today): ")

    # Zeigt die Übung nummeriert an
    show_exercise_choices(exercises)
    # Fragt die Nummer der übung ab: erlaubt ist 1 bis Anzahl Übungen
    number = validation.read_int(
        f"Exercise number (1-{len(exercises)}): ",
        1,
        len(exercises),
    )
    # Holt die gewähle Übung: Nummer 1 steht an Position 0
    exercise = exercises[number - 1]

    # Fragt die Sätze ab(ganze Zahl von 1 - 20)
    sets = validation.read_int(
        f"Sets ({MIN_SETS}-{MAX_SETS}): ",
        MIN_SETS,
        MAX_SETS,
    )

    # Fragt die Wiederholungen ab (ganze Zahl, von 1 - 100)
    reps = validation.read_int(
        f"Repetitions ({MIN_REPS}-{MAX_REPS}): ",
        MIN_REPS,
        MAX_REPS,
    )
    # Fragt das Gewicht ab (Zahl ab 0)
    weight = validation.read_weight("Weight in kg (0 = bodyweight): ")

    # Erst hier sind alle Werte geprüft: Eintrag jetzt erstellen
    # Baut ein Dictionary in gemeinsamen Format vom Team
    workout = {
        # Neue, eindeutige ID des Trainings z.B. "6"
        "id": next_workout_id(workouts),
        # ID der gewählten Übung z.B. "ex-bench"
        "exercise_id": exercise["id"],
        # Datum als Text
        "date": date,
        # Anzahl Sätze
        "sets": sets,
        # Anzahl Wiederholungen
        "reps": reps,
        # Gewicht in kg
        "weight": weight,
    }
    # Hängt genau diesen Eintrag ans Ende der Liste an
    workouts.append(workout)

    # Bestätigung US4: alle Werte anzeigen
    print("Workout saved:")
    # Datum anzeigen
    print(f" Date:   {workout['date']}")
    # Übung mit Muskelgruppe anzeigen
    print(f" Exercise:   {exercise['name']}" 
          f" ({exercise['muscle_group']})")
    # Sätze anzeigen
    print(f" Sets:   {workout['sets']}")
    # Wiederholungen anzeigen
    print(f" Repetitions:   {workout['reps']}")
    # Gewicht anzeigen
    print(f" Weight:   {workout['weight']} kg")
    #Gibt den neuen Eintrag zurück, damit main.py speichern kann
    return workout