import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands
from discord.channel import CategoryChannel, VoiceChannel, TextChannel
from discord.abc import GuildChannel

from pgbot import PGBot, guild_ids
from pgbot.utils.backup_utils import BackupUtils
from typing import List

import time
import json


class Backup(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot: PGBot = bot

    @cog_ext.cog_slash(name="backup", description="Robi backup", guild_ids=guild_ids)
    async def __backup(self, ctx: SlashContext):
        backup_data = BackupUtils.create_backup(self.bot)
        print(backup_data)


def setup(bot: PGBot):
    bot.add_cog(Backup(bot))
