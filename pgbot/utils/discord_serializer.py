from discord.channel import CategoryChannel, VoiceChannel, TextChannel
from discord.abc import GuildChannel


class DiscordSerializer:
    @staticmethod
    def serialize_category_channel(category_channel: CategoryChannel):
        data = DiscordSerializer.serialize_channel(category_channel)
        data["type"] = "category"
        data["nswf"] = category_channel.is_nsfw()
        data["text_channels"] = [DiscordSerializer.serialize_text_channel(
            tc) for tc in category_channel.text_channels]
        data["voice_channels"] = [DiscordSerializer.serialize_voice_channel(
            vc) for vc in category_channel.voice_channels]

        return data

    @staticmethod
    def serialize_voice_channel(voice_channel: VoiceChannel):
        data = DiscordSerializer.serialize_channel(voice_channel)
        data["type"] = "voice"
        data["bitrate"] = voice_channel.bitrate
        data["user_limit"] = voice_channel.user_limit
        return data

    @staticmethod
    def serialize_text_channel(text_channel: TextChannel):
        data = DiscordSerializer.serialize_channel(text_channel)
        data["type"] = "text"
        data["nsfw"] = text_channel.is_nsfw()
        data["news"] = text_channel.is_news()
        return data

    @staticmethod
    def serialize_channel(guild_channel: GuildChannel):
        data = {}
        data["name"] = guild_channel.name
        data["category"] = guild_channel.category.id if guild_channel.category else None
        data["permissions_synced"] = guild_channel.permissions_synced
        data["position"] = guild_channel.position

        data["permissions"] = []
        for overwritten_role in guild_channel.overwrites:
            role_overwrites = guild_channel.overwrites_for(overwritten_role)
            allowed_permissions, denied_permissions = role_overwrites.pair()

            role_permissions = {}
            role_permissions["role_id"] = overwritten_role.id

            role_permissions["allow"] = allowed_permissions.value
            role_permissions["deny"] = denied_permissions.value

            data["permissions"].append(role_permissions)

        return data
