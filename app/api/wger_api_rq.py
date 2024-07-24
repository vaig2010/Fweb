import requests


RU_CODE = 5
EN_CODE = 2
URL = "https://wger.de/api/v2/"

def load_data():
    response = requests.get(URL)
    all_pages = response.json()
    exercise = all_pages['exercise']
    exercise_categories = requests.get(all_pages['exercisecategory']).json()["results"]
    equipments = requests.get(all_pages['equipment']).json()["results"]
    muscles = requests.get(all_pages['muscle']).json()["results"]

def get_some_exercise(category = "", equipment: list = [],
                      muscles: list = [], language = EN_CODE) -> dict:
    # bugs with lists
    return requests.get(URL + 
                        "exercise/?category={}&language={}&equipment={}&muscles={}".format(
                            category, language, ",".join(equipment), ','.join(muscles))).json()

def BMR_calculator(height: int, weight: int, age: int, sex: str, activity_level = 0) -> int:
    """
    Calculates the Basal Metabolic Rate (BMR) based on the input parameters.

    Parameters:
        height (int): The height in centimeters.
        weight (int): The weight in kilograms.
        age (int): The age in years.
        sex (str): The gender, "М" for male and "Ж" for female.
        activity_level (int): The activity level index (default is 0).

    Returns:
        int: The calculated Basal Metabolic Rate (BMR).
    """
    ACTIVITY_LEVELS = (1.2, 1.375, 1.55, 1.725, 1.9)
    formula = 10 * weight + 6.25 * height - 5 * age
    if sex == "М":
        return round((formula + 5) * ACTIVITY_LEVELS[activity_level])
    elif sex == "Ж":
        return round((formula - 161) * ACTIVITY_LEVELS[activity_level])

#print(response.status_code)
#print(get_exercise_by_categorie(exercise_categories[0]['id']))
print(get_some_exercise())