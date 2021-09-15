from pgbot import PGBot
from pgbot import guild_ids


import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils import manage_commands


class Info(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="info", description="Wyświetla informacje o użytkowniku", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="user",
            description="Użytkownik",
            option_type=SlashCommandOptionType.USER,
            required=True
        )
    ])
    async def __info(self, ctx: SlashContext, user: discord.Member):

        info = {
            "Nick": user.name,
            "ID": user.id,
            "Status": user.status,
            "Najwyższa rola": user.top_role,
            "Dołączył/a": user.joined_at,
            "#": user.discriminator,
            "Avatar": user.avatar_url,
            "Server": user.guild
        }

        msg = ""
        for key, value in info.items():
            msg += f"{key} : {str(value)}\n"

        em = discord.Embed(
            title=f"Informacje o {info['Nick']}", description=msg, colour=discord.Colour.blue())
        await ctx.send(embed=em)


def setup(bot: PGBot):
    bot.add_cog(Info(bot))
