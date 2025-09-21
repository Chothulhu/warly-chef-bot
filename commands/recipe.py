import discord
from utils.file_handlers import save_recipes
from utils.recipe_parser import parse_recipe
from config import NOTE_EMOJI


async def handle_recipe(message, recipe_store):
    """
    Handle w@recipe: Save a recipe from a replied message.
    """
    if not message.reference:
        await message.channel.send(
            "Moraš da odgovoriš na svoju poruku da dodaš recept.",
            delete_after=5,
        )
        return

    try:
        target_message = await message.channel.fetch_message(
            message.reference.message_id
        )
    except discord.NotFound:
        await message.channel.send(
            "Nisam našao poruku na koju odgovaraš.", delete_after=5
        )
        return

    if target_message.author.id != message.author.id:
        await message.channel.send(
            "Možeš da dodaješ recepte samo na **svoje poruke**.",
            delete_after=5,
        )
        return

    raw_recipe = message.content.split("w@recipe", 1)[1].strip()
    parsed = parse_recipe(raw_recipe)

    if not any(parsed.values()):
        await message.channel.send(
            "Recept mora sadržati barem jedan tag: [ime], [sastojci] ili [priprema].",
            delete_after=8,
        )
        return

    recipe_store[str(target_message.id)] = {
        "recipe": parsed,
        "channel_id": target_message.channel.id,
    }
    save_recipes(recipe_store)

    try:
        await target_message.add_reaction(NOTE_EMOJI)
    except discord.Forbidden:
        await message.channel.send(
            "Nemam dozvolu da dodam reakciju ovde.", delete_after=5
        )

    try:
        await message.delete()
    except discord.Forbidden:
        await message.channel.send(
            "Nemam dozvolu da obrišem tvoju poruku.", delete_after=5
        )
