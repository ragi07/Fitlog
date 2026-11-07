# Das Modul erfasst neue Trainingseinträge (US4)
# und löscht falsch erfasste Einträge (US6)
# Ein Eintrag wird erst gespeichert, wenn alle Eingaben gültig sind.
# Bzw. das Löschen mit y bestätigt wurde

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
        if workout_id[:1] == "w":
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
        # Neue, eindeutige ID des Trainings z.B. "W6"
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

# Definiert find_exercise: bekommt Übungsliste und eine Übungs-ID
def find_exercise(exercises, exercise_id):
    # Gibt die Übung mit dieser ID zurück, oder None, wenn es sie nicht gibt
    # Läuft über jede Übung in der Liste
    for exercise in exercises:
        # Hat diese übung die gesuchte ID?
        if exercise["id"] == exercise_id:
            #Gefunden: Übung zurückgeben (Schleife beendet)
            return exercise
    # Schleife ist durchgelaufen, ohne etwas zu finden
    return None


# Definiert format_workout; bekommt ein Training und die Übungsliste
def format_workout(workout, exercises):
    # Baut aus einem Trainingseintrag eine lesbare Zeile 
    # Sucht die passende Übung über ihre ID
    exercise = find_exercise(exercises, workout["exercise_id"])
    # Keine Übung gefunden?
    if exercise is None:
        # Dann zeigen wir wenigstens die ID an
        name = workout["exercise_id"]
    # Sonst wurde die übung gefunden
    else:
        # Dann zeigen wir ihren Namen an
        name = exercise["name"]
    # Setzt die Zeile mit f-strings zusammen: die KLammer () erlaubt
    # den Text auf zwei Zeilen zu verteilen
    return(f"{workout['date']} | {name} | "
           f"{workout['sets']} sets x {workout['reps']} reps | "
           f"{workout['weight']} kg")


# Definiert delete_workout: bekommt Übungsliste und Trainingsliste
def delete_workout(exercises, workouts):
    # US6 zeigt alle Trainings nummeriert an und löscht genau
    # den gewählten Eintrag, aber nur nach Besätitigung mti y
    # Gibt den gelöschten Eintrag zurück oder None -> Übungen bleiben
    # Gibt es gar keine Trainings?
    if len(workouts) == 0:
        #Meldung US6
        print("No workouts to delete.")
        # Funktion beenden, nichts gelöscht
        return None
    # Überschrift aufgeben 
    print("Workouts:")
    # Läuft über alle Positionen der Liste
    for i in range(len(workouts)):
        # Gibt Nummer ab 1 und das Training als lesbare Zeile aus
        print(f" {i +1}. {format_workout(workouts[i], exercises)}")
    
    # Fragt die Nummer ab : 0 ist auch erlaubt und heisst Abbruch
    number = validation.read_int(
        f"Number of the workout to delete "
        f"(1-{len(workouts)}, 0 = cancel): ",
        0,
        len(workouts),
    )
    # Hat der User 0 eingegeben?
    if number == 0:
        #Abbruch melden
        print("Cancelled. Nothing was deleted.")
        # Funktion beenden, nichts gelöscht
        return None

    # Holt das gewählte Training (Nr 1 = Position 0), noch ohne Löschen
    selected = workouts[number - 1]
    # Fragt nach Bestätigung: True = y / False = n
    confirmed = validation.read_yes_no(
        f"Delete '{format_workout(selected, exercises)}'? (y/n): "
    )
    # Wurde mit n geantwortet?
    if not confirmed:
        # Abbruch melden
        print("Cancelled. Nothing was deleted.")
        # Funktion beenden, nichts gelöscht
        return None

    # Entfernt genau diesen Eintrag aus der Liste
    deleted = workouts.pop(number - 1)
    # Erfolg melden
    print("Workout deleted.")
    # Gibt den gelöschten Eintrag zurück, damit main.py speichern kann
    return deleted


