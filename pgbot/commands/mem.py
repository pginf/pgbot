from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from pgbot import PGBot, guild_ids
from pgbot.utils.memes.api import MemeApiHandler


class Mem(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="mem", description="Wysyła losowego mema!", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="strona",
            description="Strona z której mają zostać wybrane memy",
            option_type=SlashCommandOptionType.STRING,
            required=False,
            choices=MemeApiHandler.WEBSITES
        ),
    ])
    async def __mem(self, ctx: SlashContext, strona: str = None):
        api = MemeApiHandler.resolve_api(
            strona) if strona else MemeApiHandler.random_api()
        mem = await api.get()
        await ctx.send(embed=mem.embed)


def setup(bot: PGBot):
    bot.add_cog(Mem(bot))
