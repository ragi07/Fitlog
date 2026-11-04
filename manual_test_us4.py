# Manueller Test für US4: erfasse Trainings mit Beispieldaten
# Ich gebe absichtlich zuerst falsche Werte ein

#Lädt die Datei workouts.py mit der Funktion log_workout
import workouts

# Beispiel übungen im Team-Format
exercises = [
    # Übung 1: Bankdrücken
    {"id": "ex-bench", "name": "Bench Press", "muscle_group": "Chest"},
    # Übung 2: Kniebeuge
    {"id": "ex-squat","name": "Squat", "muscle_group": "Legs"},
    # Übung 3: Crunch (Bauch)
    {"id": "ex-crunch", "name": "Crunch", "muscle_group": "Core"},
]

# Ein schon gespeichertes Training, damit die neue ID w2 sein muss
stored = [
    # Training w1 mit Bench Press
    {"id": "w1", "exercise_id": "ex-bench", "date": "2026-11-04",
     "sets": 3, "reps": 10, "weight": 40},
]

# Überschrift für Test 1
print("Test 1: Training erfassen")
# Zeigt, wie viele Trainings es vorher gibt
print("Vorher:", len(stored), "Training(s)")
#Ruft meine Funktion auf
workouts.log_workout(exercises, stored)
# Zeigt, wie viele Trainings es nachher gibt (+1)
print("Nachher:", len(stored), "Training(s)")
# Zeigt den neuen Eintrag 
print("Neuer Eintrag", stored[-1])

#Überschrift für Test 2
print("Test 2: Keine Übungen vorhanden")
# Ruft die Funktion mit leeren Listen auf
workouts.log_workout([], [])