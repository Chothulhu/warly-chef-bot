import discord


async def handle_format(message):
    """
    Handle w@format: Send example recipe format.
    """
    example = (
        "**Format recepta:**\n"
        "[ime] Ime tvog recepta ovde\n\n"
        "[sastojci]\n"
        "- sastojak 1\n"
        "- sastojak 2\n"
        "... \n"
        "[priprema]\n"
        "Koraci pripreme tvog jela.\n"
    )

    try:
        await message.author.send(example)
        await message.channel.send(
            f"{message.author.mention}, primer je poslat u DM!",
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
            "Nemam dozvolu da obrišem tvoju poruku.", delete_after=5
        )
