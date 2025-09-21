import discord
from utils.recipe_parser import format_recipe


async def handle_get_recipe(message, recipe_store):
    """
    Handle w@get_recipe: Retrieve a recipe from a replied message.
    """
    if not message.reference:
        await message.channel.send(
            "Odgovori na poruku sa receptom koji želiš da dobiješ.",
            delete_after=5,
        )
        return

    try:
        replied_message = await message.channel.fetch_message(
            message.reference.message_id
        )
    except discord.NotFound:
        await message.channel.send(
            "Nisam našao poruku na koju odgovaraš.", delete_after=5
        )
        return

    entry = recipe_store.get(str(replied_message.id))
    if not entry:
        await message.channel.send(
            "Nema sačuvanog recepta za ovu poruku.", delete_after=5
        )
        return

    formatted = format_recipe(entry["recipe"])
    try:
        await message.author.send(
            f"Recept od korisnika **{replied_message.author.display_name}**:\n\n{formatted}"
        )
        await message.channel.send(
            f"{message.author.mention}, recept ti je poslat u DM!",
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
        pass
