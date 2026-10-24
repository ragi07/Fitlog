"""Startgerüst für das FitLog-Menü."""

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


def main():
    """Starte das Menü; Fachfunktionen werden später eingebunden."""
    while True:
        show_menu()
        choice = input("Choose an option (0-10): ").strip()

        if choice == "0":
            print("Goodbye!")
            return

        if choice not in MENU_OPTIONS:
            print("Please enter a number from 0 to 10.")
            continue

        # Platzhalter: Hier werden die Funktionen des Teams eingebunden.
        print(f"{MENU_OPTIONS[choice]}: not implemented yet.")


if __name__ == "__main__":
    main()
