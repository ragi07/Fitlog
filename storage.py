import datetime
import json
import os
from exercises import DEFAULT_EXERCISES

# Dateipfad wo alle Fitlog Daten gespeichert werden
DATA_FILE = "data/fitlog.json"
# Erlaubte Muskelgruppen
MUSCLE_GROUPS = ["Chest", "Back", "Legs", "Shoulders", "Arms", "Core"]

def save_data(data):
    """Zum Speichern der Daten in JSON"""
    # Legt den Ordner data an falls noch nicht existiert
    os.makedirs("data", exist_ok=True)

    # Zuerst in temporäre Datei schreiben, damit alte Datei bei Fehler erhalten bleibt
    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        # indent=2 --> Gut lesbare Datei / ensure_ascii=False --> Umlaute bleiben erhalten
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Erst wenn alles geschrieben ist: alte Datei ersetzen
    os.replace(temp_file, DATA_FILE)


def load_data():
    """Daten aus JSON laden"""
    # Beim ersten Start, Startdaten anlegen und speichern
    if not os.path.exists(DATA_FILE):
        data = {
            "format": "fitlog-v1",
            "exercises": DEFAULT_EXERCISES,
            "workouts": [],
            "weekly_goal": 3,
        }
        save_data(data)
        return data
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            # JSON Text --> Dict.
            data = json.load(f)
        check_data(data)
    except ValueError as error:
        # Fehlerhafte Datei: Meldung ausgeben und Programm stoppen
        print("Error in", DATA_FILE, "-", error)
        raise SystemExit(1)
    return data


def check_data(data):
    """Prüft, ob die geladenen Daten gültig sind"""
    if not isinstance(data, dict):
        raise ValueError("data must be a JSON object")
    # Alle Hauptfelder müssen vorhanden sein
    for key in ["format", "exercises", "workouts", "weekly_goal"]:
        if key not in data:
            raise ValueError("missing field: " + key)
    if data["format"] != "fitlog-v1":
        raise ValueError("unknown format")
    if not isinstance(data["exercises"], list) or not isinstance(data["workouts"], list):
        raise ValueError("exercises and workouts must be lists")
    if not is_int(data["weekly_goal"]) or not 1 <= data["weekly_goal"] <= 7:
        raise ValueError("weekly_goal must be between 1 and 7")

    exercise_ids = check_exercises(data["exercises"])
    check_workouts(data["workouts"], exercise_ids)


def check_exercises(exercises):
    """Prüft jede Übung und gibt die Liste der Übungs-IDs zurück"""
    ids = []
    names = []
    for exercise in exercises:
        if not isinstance(exercise, dict):
            raise ValueError("every exercise must be an object")
        if not is_int(exercise.get("id")) or exercise["id"] < 1 or exercise["id"] in ids:
            raise ValueError("every exercise needs a unique positive id")
        name = exercise.get("name")
        if not isinstance(name, str) or not 1 <= len(name.strip()) <= 60:
            raise ValueError("every exercise needs a name with 1-60 characters")
        if name.lower() in names:
            raise ValueError("duplicate exercise name: " + name)
        if exercise.get("muscle_group") not in MUSCLE_GROUPS:
            raise ValueError("invalid muscle group")
        ids.append(exercise["id"])
        names.append(name.lower())
    return ids


def check_workouts(workouts, exercise_ids):
    """Prüft jedes Training, auch ob die Übung existiert"""
    ids = []
    for workout in workouts:
        if not isinstance(workout, dict):
            raise ValueError("every workout must be an object")
        if not is_int(workout.get("id")) or workout["id"] < 1 or workout["id"] in ids:
            raise ValueError("every workout needs a unique positive id")
        if not is_int(workout.get("exercise_id")) or workout["exercise_id"] not in exercise_ids:
            raise ValueError("workout refers to an unknown exercise")
        if not is_valid_date(workout.get("date")):
            raise ValueError("date must be a real date in the format YYYY-MM-DD")
        if not is_int(workout.get("sets")) or not 1 <= workout["sets"] <= 20:
            raise ValueError("sets must be between 1 and 20")
        if not is_int(workout.get("reps")) or not 1 <= workout["reps"] <= 100:
            raise ValueError("reps must be between 1 and 100")
        weight = workout.get("weight")
        # NaN und unendlich sind keine gültigen Gewichte
        if not is_number(weight) or not 0 <= weight < float("inf"):
            raise ValueError("weight must be a number of at least 0")
        ids.append(workout["id"])


def is_int(value):
    """True für ganze Zahlen (True/False zählen nicht als Zahl)"""
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value):
    """True für ganze Zahlen und Kommazahlen (True/False zählen nicht)"""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_valid_date(text):
    """True, wenn text ein echtes Datum im Format YYYY-MM-DD ist"""
    try:
        # Umwandeln und zurück: nur das exakte Format YYYY-MM-DD bleibt gleich
        return datetime.date.fromisoformat(text).isoformat() == text
    except (TypeError, ValueError):
        return False


def next_id(items):
    """Vergibt neue id, höchste vorhandene ID + 1"""
    # Leere Liste --> Erste ID = 1
    if len(items) == 0:
        return 1
    return max(item["id"] for item in items) + 1


