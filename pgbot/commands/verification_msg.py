import discord.utils
from discord.ext import commands
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext, SlashContext, SlashCommandOptionType
from discord_slash.utils import manage_commands

from pgbot import PGBot, guild_ids


class VerificationMSG(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name='weryfikuj', description="weryfikacja", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="numer_albumu",
            description="numer albumu",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        ),
        manage_commands.create_option(
            name="imie",
            description="imie",
            option_type=SlashCommandOptionType.STRING,
            required=True
        ),
        manage_commands.create_option(
            name="nazwisko",
            description="nazwisko",
            option_type=SlashCommandOptionType.STRING,
            required=True
        ),
    ])
    async def __weryfikuj(self, ctx: SlashContext, numer_albumu, imie, nazwisko):
        if ctx.channel_id != 897436638869856266:
            return

        channel = self.bot.get_channel(897436666841661440)

        embed = (discord.Embed(title="Formularz",
                              description=f"Użytkownik: {ctx.author.mention}")
                .add_field(name="Imię", value=imie.title())
                .add_field(name="Nazwisko", value=nazwisko.title())
                .add_field(name="Numer albumu", value=numer_albumu)
                .add_field(name="Discord ID", value=ctx.author_id))


        buttons = [
            create_button(
                style=ButtonStyle.green,
                label="Zatwierdż"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Odrzuć",
            )
        ]

        action_row = create_actionrow(*buttons)

        await channel.send(embed=embed, components=[action_row])

        await ctx.send("Dziękuje za uzupełnienie formularza, twoje podanie wkrótce zostanie rozpatrzone", hidden=True)

def setup(bot: PGBot):
    bot.add_cog(VerificationMSG(bot))




