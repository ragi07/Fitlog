"""Startgerüst für das FitLog-Menü."""
from exercises import DEFAULT_EXERCISES, show_exercises
from analytics import show_history

MENU_OPTIONS = {
    "1": "Show exercises",
    "2": "Add exercise",
    "3": "Search exercises",
    "4": "Add workout",
    "5": "Delete workout",
    "6": "Show history",
    "7": "Show progress",
    "8": "Show volume per muscle group",
    "9": "Weekly goal",
    "10": "Export weekly report (CSV)",
    "0": "Exit",
}


def show_menu():
    """Zeige die vereinbarten Menüpunkte an."""
    print("\nFitLog")
    for number, label in MENU_OPTIONS.items():
        print(f"{number}: {label}")


def main(data=None):
    """Starte das Menü mit einem gemeinsamen Datenbestand."""
    if data is None:
        exercises = []
        for exercise in DEFAULT_EXERCISES:
            exercises.append(exercise.copy())
        data = {
            "format": "fitlog-v1",
            "exercises": exercises,
            "workouts": [],
            "weekly_goal": 3,
        }

    while True:
        show_menu()
        choice = input("Choose an option (0-10): ").strip()

        if choice == "0":
            print("Goodbye!")
            return

        if choice not in MENU_OPTIONS:
            print("Please enter a number from 0 to 10.")
            continue

        if choice == "1":
            show_exercises(data["exercises"])
        elif choice == "6":
            show_history(data)
        else:
            print(f"{MENU_OPTIONS[choice]}: not implemented yet.")


if __name__ == "__main__":
    main()
