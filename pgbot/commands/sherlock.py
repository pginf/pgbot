import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from pgbot import PGBot, guild_ids
from pgbot.lib.sherlock import sherlock


class Sherlock(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="sherlock", description="Wyświetla konta użytkownika na stronach", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="user",
            description="Nazwa użytkownika",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __sherlock(self, ctx: SlashContext, user: str):

        await ctx.defer()
        result = sherlock.get_user(user)

        desc = ""
        for r in result:
            desc += f"[🔹] **{r.site_name}:** {r.site_url_user}\n"

        if len(desc) >= 4096:
            desc = ""
            for r in result:
                desc += f"{r.site_url_user}\n"

            if len(desc) > 4096:
                desc = desc[:4095]

        em = discord.Embed(title="🕵️‍♂️ Sherlock",
                           description=desc)
        await ctx.send(embed=em)


def setup(bot: PGBot):
    bot.add_cog(Sherlock(bot))
