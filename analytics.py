"""Auswertungen für die FitLog-Trainingsdaten."""

from exercises import sort_key


def workout_date(workout):
    """Gib das Datum für die Sortierung zurück."""
    return workout["date"]


def get_history(workouts, exercise_id=None):
    """Sortiere passende Trainings, ohne die gespeicherte Liste zu ändern."""
    history = []
    for workout in workouts:
        if exercise_id is None or workout["exercise_id"] == exercise_id:
            history.append(workout)

    return sorted(history, key=workout_date)


def select_exercise(exercises, allow_all=False):
    """Wähle eine Übungs-ID. None bedeutet alle oder Abbrechen."""
    if not exercises:
        print("No exercises available.")
        return None

    if allow_all:
        print("0: (all)")
    else:
        print("0: Cancel")

    ordered_exercises = sorted(exercises, key=sort_key)
    for number, exercise in enumerate(ordered_exercises, start=1):
        print(f"{number}: {exercise['name']} ({exercise['muscle_group']})")

    while True:
        text = input("Choose an exercise: ").strip()
        try:
            number = int(text)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if number == 0:
            return None
        if 1 <= number <= len(ordered_exercises):
            return ordered_exercises[number - 1]["id"]

        print(f"Please choose a number from 0 to {len(ordered_exercises)}.")


def show_history(data):
    """Zeige die Historie mit einem optionalen Übungsfilter."""
    if not data["workouts"]:
        print("No workouts available.")
        return

    exercise_id = select_exercise(data["exercises"], allow_all=True)
    history = get_history(data["workouts"], exercise_id)
    if not history:
        print("No workouts for this exercise.")
        return

    exercise_names = {}
    for exercise in data["exercises"]:
        exercise_names[exercise["id"]] = exercise["name"]

    print("Date | Exercise | Sets | Reps | Weight")
    for workout in history:
        exercise_name = exercise_names[workout["exercise_id"]]
        print(
            f"{workout['date']} | {exercise_name} | {workout['sets']} | "
            f"{workout['reps']} | {workout['weight']:g} kg"
        )
