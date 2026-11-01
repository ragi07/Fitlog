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
    # Alle drei Felder müssen vorhanden sein
    for key in ["exercises", "workouts", "weekly_goal"]:
        if key not in data:
            raise ValueError("missing field: " + key)
    if not isinstance(data["exercises"], list) or not isinstance(data["workouts"], list):
        raise ValueError("exercises and workouts must be lists")
    if data["weekly_goal"] not in range(1, 8):
        raise ValueError("weekly_goal must be between 1 and 7")
    for exercise in data["exercises"]:
        if exercise.get("muscle_group") not in MUSCLE_GROUPS:
            raise ValueError("invalid muscle group")


def next_id(items):
    """Vergibt neue id, höchste vorhandene ID + 1"""
    # Leere Liste --> Erste ID = 1
    if len(items) == 0:
        return 1
    return max(item["id"] for item in items) + 1


