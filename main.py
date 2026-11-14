"""Hauptmenü für FitLog mit einem gemeinsamen Datenbestand."""
from exercises import show_exercises, add_exercise
from analytics import show_history, show_progress, show_volume
from goals import weekly_goal_menu
from report import export_weekly_report
from storage import load_data
from validation import read_menu_choice

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
        try:
            data = load_data()
        except OSError as error:
            print(f"Could not load the training data: {error}")
            return

    while True:
        show_menu()
        choice = str(read_menu_choice())

        if choice == "0":
            print("Goodbye!")
            return

        if choice not in MENU_OPTIONS:
            print("Please enter a number from 0 to 10.")
            continue
        if choice == "1":
            show_exercises(data["exercises"])
        elif choice == "2":
            add_exercise(data["exercises"])
        elif choice == "6":
            show_history(data)
        elif choice == "7":
            show_progress(data)
        elif choice == "8":
            show_volume(data)
        elif choice == "9":
            weekly_goal_menu(data)
        elif choice == "10":
            export_weekly_report(data)
        else:
            print(f"{MENU_OPTIONS[choice]}: not implemented yet.")


if __name__ == "__main__":
    main()

