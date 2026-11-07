# Manueller Test US6: löscht Trainings mit Beispieldaten
# Ich gebe extra zuerst falsche Werte ein

# Lädt meine Datei workouts.py mit der Funktion delete_workout
import workouts

# Beispielübungen im Team-Format
exercises = [
    # Übung 1: Bankdrücken
    {"id": "ex-bench", "name": "Bench Press", "muscle_group": "Chest"},
    # Übung 2: Rudern
    {"id": "ex-row", "name": "Rudern", "muscle_group": "Back"},
]

# Drei gespeicherte Trainings, eins davon wird gelöscht
stored = [
    # Training w1 mit Bench Press
    {"id": "w1", "exercise_id": "ex-bench", "date": "2026-11-03",
     "sets": 3, "reps": 10, "weight": 40},
     # Training w2 mit Rudern
     {"id": "w2", "exercise_id": "ex-row", "date": "2026-11-04",
     "sets": 3, "reps": 12, "weight": 30},
     # Training w3 mit Bench Press
     {"id": "w3", "exercise_id": "ex-bench", "date": "2026-11-05",
     "sets": 3, "reps": 10, "weight": 45},
]


# Überschrift für Test 1
print("Test 1: Abbrechen mit n")
#Ruft meine Funktion auf: Nummer wählen, dann mit n abbrechen
workouts.delete_workout(exercises, stored)
# Es müssen immer noch 3 Trainings da sein
print("Nachher:", len(stored), "Training(s)")

# Überschrift für Test 2
print("Test 2: Löschen mit y")
# Ruft meine Funktion nochmals auf: diesesmal mit y bestätigen
workouts.delete_workout(exercises, stored)
# Jetzt dürfen nur noch 2 Trainings da sein
print("Nachher:", len(stored), "Training(s)")
# Zeigt die IDs die übrig geblieben sind
for workout in stored:
    # Gibt die ID und die Übung jedes Trainings aus
    print("Übrig:", workout["id"], workout["exercise_id"])
# Die übungen müssen alle noch da sein
print("Übungen:", len(exercises))

# Überschrift für Test 3
print("Test 3: Keine Trainings vorhanden")
# Ruft die Funktion mit einer leeren Trainingsliste auf
workouts.delete_workout(exercises, [])
