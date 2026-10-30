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
MUSCLE_GROUPS = [
    "Chest",
    "Back",
    "Legs",
    "Shoulders",
    "Arms",
    "Core"
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

def clean_exercise_name(name):
    name = name.strip() 

    while "  " in name:
        name = name.replace("  ", " ")
        
    if len(name) < 1 or len(name) > 60:
        return None
    
    return name



def exercise_exists(exercises, name):
    for exercise in exercises:
        if exercise["name"].lower() == name.lower():
            return True

    return False

def add_exercise(exercises):
    name = input("Exercise name: ")
    name = clean_exercise_name(name)

    if name is None:
        print("Invalid exercise name.")
        return

    if exercise_exists(exercises, name):
        print("Exercise already exists.")
        return

    print("1: Chest")
    print("2: Back")
    print("3: Legs")
    print("4: Shoulders")
    print("5: Arms")
    print("6: Core")

    muscle_choice = input("Choose a muscle group (1-6): ")

    if muscle_choice not in ["1", "2", "3", "4", "5", "6"]:
        print("Please choose a number from 1 to 6.")
        return
    
    muscle_group = MUSCLE_GROUPS[int(muscle_choice) - 1]

    exercise = {
    "id": len(exercises) + 1,
    "name": name,
    "muscle_group": muscle_group
    }
    exercises.append(exercise)
    

def search_exercises(exercises):
    search_term = input("Search exercise: ")

    if search_term == "":
        show_exercises(exercises)
        return
    
    found = False

    for exercise in exercises:
                if search_term.lower() in exercise["name"].lower() or search_term.lower() in exercise["muscle_group"].lower():
                                 found = True
                                 print(f'{exercise["muscle_group"]}: {exercise["name"]}')
                
    if not found:
        print("No matches.")

                