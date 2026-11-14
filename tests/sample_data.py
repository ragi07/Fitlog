"""Erfundene, unabhängige Beispieldaten für die Statistiktests."""


def create_test_data():
    return {
        "format": "fitlog-v1",
        "exercises": [
            {"id": 10, "name": "Bench Press", "muscle_group": "Chest"},
            {"id": 20, "name": "Row", "muscle_group": "Back"},
        ],
        "workouts": [
            {"id": 1, "exercise_id": 10, "date": "2026-10-20",
             "sets": 3, "reps": 10, "weight": 45.0},
            {"id": 2, "exercise_id": 20, "date": "2026-10-15",
             "sets": 2, "reps": 12, "weight": 30.0},
            {"id": 3, "exercise_id": 10, "date": "2026-10-10",
             "sets": 3, "reps": 10, "weight": 40.0},
            {"id": 4, "exercise_id": 10, "date": "2026-10-20",
             "sets": 2, "reps": 8, "weight": 47.5},
        ],
        "weekly_goal": 3,
    }
