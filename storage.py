import json
import os
from exercises import DEFAULT_EXERCISES

# Dateipfad wo alle Fitlog Daten gespeichert werden
DATA_FILE = "data/fitlog.json"

def save_data(data):
    """Zum Sepeichern der Daten in JSON"""
    # Legt den Ordner data an falls noch nicht exisiert
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # indent=2 -->Gut lesbare Datei / ensure_ascii=False -->Umlaute bleiben erhalten
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_data():
    """Daten aus JSONN laden"""
    # Beim Ersten Start, Startdaten anlegen und saven
    if not os.path.exists(DATA_FILE):
        data = {
            "exercises": DEFAULT_EXERCISES,
            "workouts": [],
            "weekly_goal": 3,
        }
        save_data(data)
        return data
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        # JSON Text --> Dict.
        return json.load(f)


def next_id(items):
    """Vergibt neue id, Letzte ID + 1"""
    # Leere Liste --> Erste ID = 1
    if len(items) == 0:
        return 1
    return items[-1]["id"] + 1

if __name__ == "__main__":
    # Nur zum Testen während Developement
    # PK --> Diesen Part léschen sobald main Funktionen verwendet
    data = load_data()
    print("Nächste übungid:", next_id(data["exercises"]))
    print("nächste trainigid", next_id(data["workouts"]))

