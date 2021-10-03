from discord.channel import CategoryChannel, VoiceChannel, TextChannel
from discord.abc import GuildChannel
from pgbot import PGBot
from pgbot.utils.discord_serializer import DiscordSerializer
import json
import time


class BackupUtils:
    @staticmethod
    def create_backup(bot: PGBot):
        category_channels: List[CategoryChannel] = []
        text_channels: List[TextChannel] = []
        voice_channels: List[VoiceChannel] = []

        for channel in bot.get_all_channels():
            channel_type = type(channel)
            if channel_type is CategoryChannel:
                category_channels.append(channel)
            elif channel_type is TextChannel:
                text_channels.append(channel)
            elif channel_type is VoiceChannel:
                voice_channels.append(channel)

        backup_data = {}
        backup_data["data"] = []
        backup_data["created_at"] = time.time()

        category_channels.sort(key=lambda x: x.position)
        for category_channel in category_channels:
            category = DiscordSerializer.serialize_category_channel(
                category_channel)

            category["text_channels"].sort(
                key=lambda channel: channel["position"])
            category["voice_channels"].sort(
                key=lambda channel: channel["position"])

            backup_data["data"].append(category)

        return json.dumps(backup_data, ensure_ascii=False)
