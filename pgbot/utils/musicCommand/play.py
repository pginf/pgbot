from pgbot import PGBot
from pgbot import guild_ids

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils import manage_commands


class Play(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="play", description="Odtwarzanie muzyki.", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="song",
            description="Link/nazwa utworu",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __play(self, ctx: SlashContext, song: str):
        await ctx.defer()

        em = discord.Embed(
            title=f"Witaj, {ctx.author}", description=f"{song}", colour=discord.Colour.green())
        await ctx.send(embed=em)


def setup(bot: PGBot):
    bot.add_cog(Play(bot))
