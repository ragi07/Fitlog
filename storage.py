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

    check_exercises(data["exercises"])


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


def is_int(value):
    """True für ganze Zahlen (True/False zählen nicht als Zahl)"""
    return isinstance(value, int) and not isinstance(value, bool)


def next_id(items):
    """Vergibt neue id, höchste vorhandene ID + 1"""
    # Leere Liste --> Erste ID = 1
    if len(items) == 0:
        return 1
    return max(item["id"] for item in items) + 1


