import re


def parse_recipe(text):
    """
    Parses a recipe string into its components based on tags.

    Recognized tags:
        - [ime]: Name of the recipe
        - [sastojci]: Ingredients
        - [priprema]: Preparation instructions

    Args:
        text (str): The raw recipe text containing tags.

    Returns:
        dict: A dictionary with keys 'ime', 'sastojci', 'priprema'.
              Each key maps to the corresponding text if found,
              else None.
    """
    parsed = {}
    for field in ["ime", "sastojci", "priprema"]:
        match = re.search(
            rf"\[{field}\](.+?)(?=\[\w+\]|$)",  # Match content until next tag or end
            text,
            re.DOTALL | re.IGNORECASE,  # Dot matches newlines, ignore case
        )
        parsed[field] = match.group(1).strip() if match else None
    return parsed


def format_recipe(recipe):
    """
    Formats a parsed recipe dictionary into a human-readable string.

    Args:
        recipe (dict): Dictionary containing recipe fields
        'ime', 'sastojci', 'priprema'.

    Returns:
        str: Formatted multi-line string suitable for sending in Discord
        messages.
    """
    parts = []

    # Add recipe name
    if "ime" in recipe and recipe["ime"]:
        parts.append(f"{recipe['ime']}")

    # Add ingredients section if present
    if "sastojci" in recipe and recipe["sastojci"]:
        parts.append(f"\nSastojci:\n{recipe['sastojci']}")

    # Add preparation instructions if present
    if "priprema" in recipe and recipe["priprema"]:
        parts.append(f"\nPriprema:\n{recipe['priprema']}")

    return "\n".join(parts)
