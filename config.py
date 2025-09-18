import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# -----------------------------
# Discord Bot Configuration
# -----------------------------
# The bot token is stored in the .env file for security reasons
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Emoji used to mark messages with saved recipes
NOTE_EMOJI = "📒"

# Path to the JSON file where recipes are stored
RECIPE_FILE = "data/recipes.json"
