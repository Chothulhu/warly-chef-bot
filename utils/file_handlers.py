import json
import os
from config import RECIPE_FILE


def load_recipes():
    """
    Loads recipes from the JSON file.

    Returns:
        dict: A dictionary containing all saved recipes.
              Returns an empty dictionary if the file does not exist
              or is empty.
    """
    if os.path.exists(RECIPE_FILE):
        try:
            with open(RECIPE_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    # Return empty dict if file is empty
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            # Return empty dict if JSON is invalid
            return {}
    # Return empty dict if file does not exist
    return {}


def save_recipes(recipes):
    """
    Saves the given recipes dictionary to a JSON file.

    Args:
        recipes (dict): Dictionary of recipes to save.
    """
    with open(RECIPE_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)
