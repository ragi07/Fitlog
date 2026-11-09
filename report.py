import csv
import datetime
import os

from goals import week_start, count_training_days

# Ordner für die CSV-Berichte
REPORT_FOLDER = "reports"
# Spalten in der vorgegebenen Reihenfolge
HEADER = ["date", "exercise", "muscle_group", "sets", "reps",
          "weight", "volume"]


def make_safe(text):
    """Setzt ein ' vor Text, den Excel sonst als Formel ausführen würde"""
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def find_exercise(exercises, exercise_id):
    """Gibt die Übung mit dieser ID zurück"""
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            return exercise
    return None


def export_weekly_report(data, today=None):
    """Exportiert die Trainings der laufenden Woche als CSV (US12)"""
    # today kann man zum Testen mitgeben, sonst gilt das heutige Datum
    if today is None:
        today = datetime.date.today()
    monday = week_start(today)
    sunday = monday + datetime.timedelta(days=6)

    # ISO-Jahr und ISO-Kalenderwoche passen auch beim Jahreswechsel
    year, week, weekday = today.isocalendar()
    path = f"{REPORT_FOLDER}/weekly_report_{year}_CW{week:02d}.csv"

    # Eine Zeile pro Training von Montag bis Sonntag
    rows = []
    total_volume = 0
    for workout in data["workouts"]:
        day = datetime.date.fromisoformat(workout["date"])
        if monday <= day <= sunday:
            exercise = find_exercise(data["exercises"], workout["exercise_id"])
            volume = workout["sets"] * workout["reps"] * workout["weight"]
            total_volume += volume
            rows.append([
                workout["date"],
                make_safe(exercise["name"]),
                make_safe(exercise["muscle_group"]),
                workout["sets"],
                workout["reps"],
                workout["weight"],
                volume,
            ])

    try:
        os.makedirs(REPORT_FOLDER, exist_ok=True)
        # "w" ersetzt einen alten Bericht derselben Woche
        # utf-8-sig: Excel zeigt damit Umlaute richtig an
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(HEADER)
            writer.writerows(rows)
    except OSError:
        print("Could not write the report. Is the file open in Excel?")
        return None

    if len(rows) == 0:
        print("No workouts this week. The file only contains the header row.")

    # Zusammenfassung nach dem Export
    training_days = count_training_days(data["workouts"], monday)
    goal = data["weekly_goal"]
    print(f"Report saved: {path}")
    print(f"Training days: {training_days}")
    print(f"Total volume: {total_volume} kg")
    if training_days >= goal:
        print(f"Weekly goal ({goal} days): reached")
    else:
        print(f"Weekly goal ({goal} days): not reached")
    return path
