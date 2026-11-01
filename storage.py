import json
import os
from exercises import DEFAULT_EXERCISES

# Dateipfad wo alle Fitlog Daten gespeichert werden
DATA_FILE = "data/fitlog.json"

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
    """Vergibt neue id, höchste vorhandene ID + 1"""
    # Leere Liste --> Erste ID = 1
    if len(items) == 0:
        return 1
    return max(item["id"] for item in items) + 1


