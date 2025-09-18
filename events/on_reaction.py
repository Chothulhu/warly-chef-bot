import discord
from utils.recipe_parser import format_recipe


async def handle_reaction_add(bot, payload, recipe_store, NOTE_EMOJI):
    """
    Handles the addition of reactions to messages.

    If a user reacts with the NOTE_EMOJI on a message
    that has a saved recipe, the bot sends the recipe to the user via DM.

    Args:
        bot (commands.Bot): The Discord bot instance.
        payload (discord.RawReactionActionEvent): The raw reaction
        event payload.
        recipe_store (dict): Dictionary containing saved recipes.
        NOTE_EMOJI (str): The emoji used to trigger
        sending a recipe (📒).
    """

    # Ignore bot reactions and reactions that aren't the NOTE_EMOJI
    if payload.user_id == bot.user.id or str(payload.emoji.name) != NOTE_EMOJI:
        return

    message_id = str(payload.message_id)
    entry = recipe_store.get(message_id)
    if not entry:
        # No recipe associated with this message
        return

    # Get guild, channel, and user objects
    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)
    user = guild.get_member(payload.user_id) if guild else None

    # Ignore reactions from bots or invalid users
    if not user or user.bot:
        return

    try:
        # Send the recipe to the user via DM
        formatted = format_recipe(entry["recipe"])
        await user.send(f"Recept:\n\n{formatted}")
    except discord.Forbidden:
        # If bot can't DM the user, notify them in the channel
        try:
            message = await channel.fetch_message(payload.message_id)
            await message.channel.send(
                f"{user.mention}, ne mogu da ti pošaljem recept u DM. "
                "Proveri podešavanja privatnosti.",
                delete_after=5,
            )
        except Exception:
            # Fail silently if even this fails
            pass
