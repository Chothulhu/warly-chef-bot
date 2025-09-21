import discord


async def handle_help(message):
    """
    Handle w@help: Send help message with all commands.
    """
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
            "Nemam dozvolu da obrišem tvoju poruku.", delete_after=5
        )
