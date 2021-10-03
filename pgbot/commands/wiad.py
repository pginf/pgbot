from discord_slash.utils.manage_components import create_actionrow, create_button

from pgbot import PGBot
from pgbot import guild_ids


import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext, ButtonStyle
from discord_slash.utils import manage_commands


class Wiad(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="wiad", description="Wyświetla informacje o użytkowniku", guild_ids=guild_ids)
    async def __wiad(self, ctx: SlashContext):
        max_buttons_in_row = 5
        num_of_groups = 7
        left_groups = num_of_groups
        rows = []
        for row_id in range(num_of_groups // max_buttons_in_row + 1):
            if left_groups >= num_of_groups:
                buttons = (create_button(style=ButtonStyle.blue, label=str(row_id * max_buttons_in_row + i + 1)) for i in range(max_buttons_in_row))
            else:
                buttons = (create_button(style=ButtonStyle.blue, label=str(row_id * max_buttons_in_row + i + 1)) for i
                           in range(left_groups))
            left_groups -= max_buttons_in_row
            rows.append(create_actionrow(*buttons))

        await ctx.send("My Message", components=rows)



def setup(bot: PGBot):
    bot.add_cog(Wiad(bot))
