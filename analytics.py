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


def get_progress(workouts, exercise_id):
    """Vergleiche das erste und letzte Gewicht der gewählten Übung."""
    history = get_history(workouts, exercise_id)
    if len(history) < 2:
        return None

    first_weight = history[0]["weight"]
    last_weight = history[-1]["weight"]
    best_weight = first_weight

    for workout in history:
        if workout["weight"] > best_weight:
            best_weight = workout["weight"]

    return {
        "first_weight": first_weight,
        "last_weight": last_weight,
        "best_weight": best_weight,
        "progress": last_weight - first_weight,
    }


def show_progress(data):
    """Zeige die Gewichte und ihre Veränderung für eine einzelne Übung."""
    exercise_id = select_exercise(data["exercises"])
    if exercise_id is None:
        return

    progress = get_progress(data["workouts"], exercise_id)
    if progress is None:
        print("Not enough entries (at least 2 needed).")
        return

    print(f"First weight: {progress['first_weight']:g} kg")
    print(f"Last weight: {progress['last_weight']:g} kg")
    print(f"Best weight: {progress['best_weight']:g} kg")
    print(f"Progress: {progress['progress']:+g} kg")
