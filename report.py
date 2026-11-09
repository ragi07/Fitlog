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
