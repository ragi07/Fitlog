import json
import os

# Dateipfad wo alle Fitlog Daten gespeichert werden
DATA_FILE = "data/fitlog.json"

def save_data(data):
    """Zum Sepeichern der Daten in JSON"""
# Legt den Ordner data an falls noch nicht exisiert
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # indent=2 -->Gut lesbare Datei / ensure_ascii=False -->Umlaute bleiben erhalten
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Nur zum Testen während Developement
    # PK --> Diesen Part léschen sobald main Funktionen verwendet
    test_data = {
        "exercises": [{"id": 1, "name": "übung test", "muscle_group": "Chest"}],
        "workouts": [],
        "weekly_goal": 3,
    }
    save_data(test_data)
    print("Gespeichert in", DATA_FILE)

