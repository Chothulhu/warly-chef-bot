import discord
from utils.file_handlers import save_recipes
from utils.recipe_parser import parse_recipe, format_recipe
from config import NOTE_EMOJI


async def handle_message(bot, message, recipe_store):
    """
    Handles incoming messages and executes commands for the Warly Bot.

    Supported commands:
        - w@recipe: Save a recipe from a replied message.
        - w@get_recipe: Retrieve a recipe from a replied message.
        - w@recipes: List all saved recipes or get a recipe by name.
        - w@format: Send an example recipe format to the user.
        - w@help: Send a help message with all commands.

    Args:
        bot (commands.Bot): The Discord bot instance.
        message (discord.Message): The message received.
        recipe_store (dict): Dictionary containing saved recipes.
    """

    # Ignore messages sent by bots
    if message.author.bot:
        return

    content_lower = message.content.lower().strip()

    # --- w@recipe: Save a recipe ---
    if content_lower.startswith("w@recipe") and message.reference:
        try:
            target_message = await message.channel.fetch_message(
                message.reference.message_id
            )
        except discord.NotFound:
            await message.channel.send(
                "Couldn't find the message you're replying to.", delete_after=5
            )
            return

        # Ensure user is saving recipe for their own message
        if target_message.author.id != message.author.id:
            await message.channel.send(
                "You can only attach recipes to **your own** posts.",
                delete_after=5,
            )
            return

        parts = message.content.split("w@recipe", 1)
        if len(parts) > 1:
            raw_recipe = parts[1].strip()
            parsed = parse_recipe(raw_recipe)

            if not any(parsed.values()):
                await message.channel.send(
                    "Recept mora sadržati barem jedan tag: "
                    "[ime], [sastojci] ili [priprema].",
                    delete_after=8,
                )
                return

            # Save the recipe to the store and persist it
            recipe_store[str(target_message.id)] = {
                "recipe": parsed,
                "channel_id": target_message.channel.id,
            }
            save_recipes(recipe_store)

            # Add the note emoji to the original message
            try:
                await target_message.add_reaction(NOTE_EMOJI)
            except discord.Forbidden:
                await message.channel.send(
                    "I don't have permission to add reactions here.",
                    delete_after=5,
                )

            # Attempt to delete the command message
            try:
                await message.delete()
            except discord.Forbidden:
                await message.channel.send(
                    "I don't have permission to delete messages here.",
                    delete_after=5,
                )
            else:
                await message.channel.send(
                    "Recept sačuvan! (poruka obrisana)", delete_after=5
                )

    # --- w@get_recipe: Retrieve a recipe ---
    elif content_lower.startswith("w@get_recipe") and message.reference:
        try:
            replied_message = await message.channel.fetch_message(
                message.reference.message_id
            )
        except discord.NotFound:
            await message.channel.send(
                "Couldn't find the message you're replying to.", delete_after=5
            )
            return

        entry = recipe_store.get(str(replied_message.id))
        if entry:
            formatted = format_recipe(entry["recipe"])
            try:
                await message.author.send(
                    f"Recept od korisnika **{replied_message .author .display_name}**:\n\n{formatted}"
                )
                await message.channel.send(
                    f"{message.author.mention}, pogledaj DM!", delete_after=5
                )
            except discord.Forbidden:
                await message.channel.send(
                    "Ne mogu ti poslati DM. "
                    "Proveri podešavanja privatnosti.",
                    delete_after=5,
                )
        else:
            await message.channel.send(
                "Nema sačuvanog recepta za ovu poruku.", delete_after=5
            )

        try:
            await message.delete()
        except discord.Forbidden:
            pass

    # --- w@recipes: List recipes or fetch by name ---
    elif content_lower.startswith("w@recipes"):
        args = message.content.split(" ", 1)

        # User requested list of all recipes
        if len(args) == 1:
            names = []
            for entry in recipe_store.values():
                recipe_data = entry.get("recipe", {})
                name = recipe_data.get("ime")
                if name:
                    names.append(f"- {name}")
            if not names:
                await message.channel.send(
                    "Nema sačuvanih recepata.", delete_after=5
                )
                return
            try:
                await message.author.send(
                    "**Lista sačuvanih recepata:**\n" + "\n".join(names)
                )
                await message.channel.send(
                    f"{message.author.mention}, pogledaj DM!", delete_after=5
                )
            except discord.Forbidden:
                await message.channel.send(
                    "Ne mogu da ti pošaljem DM. "
                    "Proveri podešavanja privatnosti.",
                    delete_after=5,
                )

        # User requested a specific recipe by name
        else:
            search_term = args[1].strip().lower()
            found = None
            for entry in recipe_store.values():
                recipe_data = entry.get("recipe", {})
                name = recipe_data.get("ime", "").lower()
                if name == search_term:
                    found = recipe_data
                    break
            if found:
                try:
                    await message.author.send(
                        f"Recept:\n\n{format_recipe(found)}"
                    )
                    await message.channel.send(
                        f"{message.author.mention}, recept je poslat u DM!",
                        delete_after=5,
                    )
                except discord.Forbidden:
                    await message.channel.send(
                        "Ne mogu da ti pošaljem DM. "
                        "Proveri podešavanja privatnosti.",
                        delete_after=5,
                    )
            else:
                await message.channel.send(
                    "Nije pronađen nijedan recept sa tim imenom.",
                    delete_after=5,
                )
        try:
            await message.delete()
        except discord.Forbidden:
            await message.channel.send(
                "I don't have permission to delete messages here.",
                delete_after=5,
            )

    # --- w@format: Send example recipe format ---
    elif content_lower.startswith("w@format"):
        example = (
            "**Format recepta:** (uglaste zagrade i tekst u njima su tagovi koje treba ispoštovati)\n"
            "[ime] Ime tvog recepta ovde\n\n"
            "[sastojci]\n"
            "- sastojak 1\n"
            "- sastojak 2\n"
            "... \n"
            "[priprema]\n"
            "Koraci ili nabacan tekst koji opisuje pripremu tvog jela ovde.\n"
        )
        try:
            await message.author.send(example)
            await message.channel.send(
                f"{message.author.mention}, primer je poslat u DM!",
                delete_after=5,
            )
        except discord.Forbidden:
            await message.channel.send(
                "Ne mogu da ti pošaljem DM. "
                "Proveri podešavanja privatnosti.",
                delete_after=5,
            )
        try:
            await message.delete()
        except discord.Forbidden:
            await message.channel.send(
                "I don't have permission to delete messages here.",
                delete_after=5,
            )

    # --- w@help: Send help message ---
    elif content_lower.startswith("w@help"):
        help_text = (
            "**Warly Bot Komande:**\n\n"
            "`w@recipe` – Odgovori na svoju poruku i dodaj recept koristeći tagove [ime], [sastojci], [priprema].\n"
            "`w@get_recipe` – Odgovori na poruku sa receptom i dobićeš recept u DM.\n"
            "Reaguj na poruku sa 📒 da dobiješ recept u DM (ako postoji).\n"
            "`w@recipes` – Prikazuje listu svih sačuvanih recepata.\n"
            "`w@recipes <ime>` – Pošalje recept sa tim imenom u DM (ako postoji).\n"
            "`w@format` – Primer kako formatirati recept sa tagovima.\n"
            "`w@help` – Prikazuje ovu poruku sa uputstvima.\n"
        )
        try:
            await message.author.send(help_text)
            await message.channel.send(
                f"{message.author.mention}, spisak komandi je poslat u DM!",
                delete_after=5,
            )
        except discord.Forbidden:
            await message.channel.send(
                "Ne mogu da ti pošaljem DM. Proveri podešavanja privatnosti.",
                delete_after=5,
            )

        try:
            await message.delete()
        except discord.Forbidden:
            await message.channel.send(
                "I don't have permission to delete messages here.",
                delete_after=5,
            )

    # Process commands if any were invoked directly
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
