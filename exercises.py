DEFAULT_EXERCISES = [
    {
        "id": 1,
        "name": "Bench Press",
        "muscle_group": "Chest"
    },            
        {
        "id": 2,
        "name": "Pull Up",
        "muscle_group": "Back"
    },
    {
        "id": 3,
        "name": "Squat",
        "muscle_group": "Legs"
    },
    {
        "id": 4,
        "name": "Shoulder Press",
        "muscle_group": "Shoulders"
    },
    {
        "id": 5,
        "name": "Bicep Curl",
        "muscle_group": "Arms"
    },
    {
        "id": 6,
        "name": "Plank",
        "muscle_group": "Core"
    }
]


def show_exercises(exercises):
        if not exercises:
            print("No exercises available.")
            return

        
        sorted_exercises = sorted(exercises, key=sort_key)
    
    
        for exercise in sorted_exercises:
            print(
            f'{exercise["muscle_group"]}: {exercise["name"]}'
            )
        
def sort_key(exercise):
    return exercise["muscle_group"], exercise["name"]

