import discord
from utils.recipe_parser import format_recipe


async def handle_recipes(message, recipe_store):
    """
    Handle w@recipes: List all recipes or get by name.
    """
    args = message.content.split(" ", 1)

    # List all saved recipes
    if len(args) == 1:
        names = []
        for entry in recipe_store.values():
            recipe_data = entry.get("recipe", {})
            if recipe_data.get("ime"):
                names.append(f"- {recipe_data['ime']}")

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
                "Ne mogu da ti pošaljem DM. Proveri podešavanja privatnosti.",
                delete_after=5,
            )
        return

    # Search recipe by name
    search_term = args[1].strip().lower()
    found = None
    for entry in recipe_store.values():
        recipe_data = entry.get("recipe", {})
        if recipe_data.get("ime", "").lower() == search_term:
            found = recipe_data
            break

    print(found)
    if found:
        try:
            await message.author.send(f"Recept:\n\n{format_recipe(found)}")
            await message.channel.send(
                f"{message.author.mention}, recept je poslat u DM!",
                delete_after=5,
            )
        except discord.Forbidden:
            await message.channel.send(
                "Ne mogu da ti pošaljem DM. Proveri podešavanja privatnosti.",
                delete_after=5,
            )
    else:
        await message.channel.send(
            "Nije pronađen nijedan recept sa tim imenom.", delete_after=5
        )

    try:
        await message.delete()
    except discord.Forbidden:
        await message.channel.send(
            "Nemam dozvolu da obrišem tvoju poruku.", delete_after=5
        )
