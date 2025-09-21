from commands import recipe, get_recipe, recipes, format, help

COMMANDS = {
    "w@recipes": recipes.handle_recipes,
    "w@get_recipe": get_recipe.handle_get_recipe,
    "w@recipe": recipe.handle_recipe,
    "w@format": format.handle_format,
    "w@help": help.handle_help,
}


async def handle_message(bot, message, recipe_store):
    if message.author.bot:
        return

    content = message.content.strip()

    command = next(
        (command for command in COMMANDS if content.startswith(command)), None
    )

    if command:
        handler = COMMANDS[command]

        if command in ("w@format", "w@help"):
            await handler(message)
        else:
            await handler(message, recipe_store)
