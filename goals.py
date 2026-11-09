import datetime

from storage import save_data
from validation import read_int, read_yes_no


def week_start(day):
    """Gibt den Montag der Woche zurück"""
    # weekday(): Montag = 0 ... Sonntag = 6
    return day - datetime.timedelta(days=day.weekday())


def count_training_days(workouts, monday):
    """Zählt die Trainingstage von Montag bis Sonntag"""
    sunday = monday + datetime.timedelta(days=6)
    # set: gleicher Tag zählt nur einmal
    days = set()
    for workout in workouts:
        day = datetime.date.fromisoformat(workout["date"])
        if monday <= day <= sunday:
            days.add(day)
    return len(days)


def count_streak(workouts, goal):
    """Zählt Wochen in Folge mit erreichtem Ziel (ohne aktuelle Woche)"""
    # Mit der Vorwoche beginnen und rückwärts zählen
    monday = week_start(datetime.date.today()) - datetime.timedelta(days=7)
    streak = 0
    while count_training_days(workouts, monday) >= goal:
        streak += 1
        monday -= datetime.timedelta(days=7)
    return streak


def weekly_goal_menu(data):
    """Menüpunkt 9: Wochenziel anzeigen und optional ändern"""
    goal = data["weekly_goal"]
    days = count_training_days(data["workouts"], week_start(datetime.date.today()))
    print(f"Training days this week: {days} of {goal}")
    print(f"Streak: {count_streak(data['workouts'], goal)} week(s) in a row")

    if read_yes_no("Change weekly goal? (y/n): "):
        new_goal = read_int("New weekly goal (1-7): ", 1, 7)
        if read_yes_no(f"Change weekly goal to {new_goal}? (y/n): "):
            data["weekly_goal"] = new_goal
            try:
                save_data(data)
                print("Weekly goal saved.")
            except OSError:
                # Speichern fehlgeschlagen --> altes Ziel behalten
                data["weekly_goal"] = goal
                print("Error: weekly goal could not be saved.")
