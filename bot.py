import discord
from discord.ext import commands
from config import TOKEN, NOTE_EMOJI
from utils.file_handlers import load_recipes
from events.on_ready import handle_on_ready
from events.on_message import handle_message
from events.on_reaction import handle_reaction_add

# -----------------------------
# Configure bot intents
# -----------------------------
intents = discord.Intents.all()  # Enable all intents
intents.message_content = True  # Needed to read message content
intents.reactions = True  # Needed to track reactions
intents.messages = True  # Needed to handle messages
intents.guilds = True  # Needed to access guild info

# Create bot instance
bot = commands.Bot(command_prefix="w@", intents=intents, help_command=None)

# Load saved recipes from JSON file
recipe_store = load_recipes()


# -----------------------------
# Events
# -----------------------------
@bot.event
async def on_ready():
    """
    Event handler called when the bot has finished connecting and is
    ready.

    Calls the on_ready handler to:
      - Re-add the 📒 emoji to messages with recipes if missing
      - Remove stale or invalid recipe entries
    """
    await handle_on_ready(bot, recipe_store, NOTE_EMOJI)


@bot.event
async def on_message(message):
    """
    Event handler called on every message the bot can see.

    Passes the message to the centralized handle_message function
    which manages all bot commands like w@recipe, w@get_recipe, etc.
    """
    await handle_message(bot, message, recipe_store)


@bot.event
async def on_raw_reaction_add(payload):
    """
    Event handler called when a reaction is added to a message.

    If the reaction is the NOTE_EMOJI (📒) and the message has a saved
    recipe, the bot sends the recipe to the user via DM.
    """
    await handle_reaction_add(bot, payload, recipe_store, NOTE_EMOJI)


# -----------------------------
# Run bot
# -----------------------------
if __name__ == "__main__":
    bot.run(TOKEN)
