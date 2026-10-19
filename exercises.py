DEFAULT_EXERCISES = [
    {
        "name": "Bench Press",
        "muscle_group": "Chest"
    },            
        {
        "name": "Pull Up",
        "muscle_group": "Back"
    },
    {
        "name": "Squat",
        "muscle_group": "Legs"
    },
    {
        "name": "Shoulder Press",
        "muscle_group": "Shoulders"
    },
    {
        "name": "Bicep Curl",
        "muscle_group": "Arms"
    },
    {
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

