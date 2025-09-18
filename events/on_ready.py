import discord
from utils.file_handlers import save_recipes


async def handle_on_ready(bot, recipe_store, NOTE_EMOJI):
    """
    Handles actions when the bot is ready.

    For each saved recipe in recipe_store:
        - Attempts to fetch the message it is associated with.
        - Re-adds the NOTE_EMOJI reaction if it is missing.
        - Removes entries for messages or channels that no longer exist
          or can't be accessed by the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.
        recipe_store (dict): Dictionary containing saved recipes.
        NOTE_EMOJI (str): The emoji used to mark
        messages with saved recipes.
    """

    to_remove = []

    for message_id_str, entry in recipe_store.items():
        try:
            # Fetch the channel from the stored channel_id
            channel_id = entry["channel_id"]
            channel = bot.get_channel(channel_id)
            if not channel:
                # Channel no longer exists; mark for removal
                to_remove.append(message_id_str)
                continue

            # Fetch the original message
            message = await channel.fetch_message(int(message_id_str))

            # Check if the message already has the
            # NOTE_EMOJI reaction from the bot
            has_note = any(
                r.emoji == NOTE_EMOJI and r.me for r in message.reactions
            )

            if not has_note:
                # Re-add the NOTE_EMOJI reaction
                await message.add_reaction(NOTE_EMOJI)

        except (discord.NotFound, discord.Forbidden):
            # Message not found or bot lacks permissions;
            # mark for removal
            to_remove.append(message_id_str)
        except Exception:
            # Ignore unexpected errors to avoid crashing on startup
            pass

    # Remove invalid or inaccessible recipe entries
    if to_remove:
        for msg_id in to_remove:
            recipe_store.pop(msg_id, None)
        # Save the updated recipe store
        save_recipes(recipe_store)
