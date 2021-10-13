import csv
from typing import List

from pgbot import PGBot
from pgbot import guild_ids

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils import manage_commands
from pgbot.db.session import session
from pgbot.db.models import PGStudent


class Album(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="album", description="Wyświetla informacje o użytkowniku", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="nr_albumu",
            description="Numer Albumu",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def __album(self, ctx: SlashContext, nr_albumu: int):
        student: PGStudent = session.query(PGStudent).filter_by(nr_albumu=nr_albumu).first()
        await ctx.send(f"{student.nr_albumu}: {student.imie} {student.nazwisko} {student.discord_id}")


def setup(bot: PGBot):
    bot.add_cog(Album(bot))
