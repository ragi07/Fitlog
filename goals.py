import datetime


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
