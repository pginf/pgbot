import random

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component, ComponentContext
from discord_slash.model import ButtonStyle

from pgbot import PGBot, guild_ids
import pgbot.utils.colors as colors
from typing import List


class Teams(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="teams", guild_ids=guild_ids, description="Losowanie drużyn", options=[
        manage_commands.create_option(
            name="ilosc_druzyn",
            description="Ilość drużyn",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def __teams(self, ctx: SlashContext, ilosc_druzyn: int):

        if ilosc_druzyn < 2:
            await ctx.send("Musi byś więcej niż 1 drużyna!")
            return

        em = discord.Embed(
            title="Losowanie Drużyn",
            description="ABY **DOŁĄCZYĆ** :white_check_mark:\n**KONIEC** CZEKANIA :x:",
            colour=colors.main
        )
        join_button = create_button(
            style=ButtonStyle.green, label="Dołącz", emoji="\u2705")
        leave_button = create_button(
            style=ButtonStyle.danger, label="Wyjdź", emoji="⛔")
        end_button = create_button(
            style=ButtonStyle.gray, label="Losuj", emoji="🎲")

        action_row = create_actionrow(join_button, leave_button, end_button)

        message = await ctx.send(embed=em, components=[action_row])

        users: List[discord.User] = []
        while True:
            button_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row)
            if button_ctx.component_id == join_button["custom_id"]:
                if button_ctx.author not in users:
                    users.append(button_ctx.author)
            elif button_ctx.component_id == leave_button["custom_id"]:
                if button_ctx.author in users:
                    users.remove(button_ctx.author)

            elif button_ctx.component_id == end_button["custom_id"] and button_ctx.author_id == ctx.author_id:
                await button_ctx.edit_origin(embed=em)
                break

            em = discord.Embed(
                title="Losowanie drużyn",
                description=f"Gracze: {', '.join((user.mention for user in users))}",
                colour=colors.main
            )

            await button_ctx.edit_origin(embed=em)
        random.shuffle(users)

        teams: List[List[discord.User]] = [[] for _ in range(ilosc_druzyn)]
        for i, user in enumerate(users):
            team = i % ilosc_druzyn
            teams[team].append(user)

        message = await ctx.channel.fetch_message(message.id)
        await message.delete()  # usuwanie wcześniej wysłanych wiadomości

        full_desc = ""
        for i, team in enumerate(teams):
            team_users_desc = ", ".join((user.mention for user in team))
            full_desc += f"Team {i+1}\n"
            full_desc += team_users_desc + "\n"
            full_desc += "\n"

        em = discord.Embed(
            title="Teams", description=full_desc, color=colors.main)
        await ctx.channel.send(embed=em)


def setup(bot: PGBot):
    bot.add_cog(Teams(bot))
