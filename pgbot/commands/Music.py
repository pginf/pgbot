from discord.ext import commands
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType
from discord_slash.utils import manage_commands

from pgbot import PGBot, guild_ids
from pgbot.lib.musicCommand.VoiceState import VoiceState


class Music(commands.Cog):
    def __init__(self, bot: PGBot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: SlashContext):
        state = self.voice_states.get(ctx.guild.id)

        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    async def cog_before_invoke(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: SlashContext, error: commands.CommandError):
        await ctx.send('Nadarzył się problem: {}'.format(str(error)))

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Tej komendy nie można użyć w prywatnej wiadomości.')

        return True

    @cog_ext.cog_slash(name='join', description='Dołączam do kanału', guild_ids=guild_ids, options=[])
    async def _join(self, ctx: SlashContext):
        # await ctx.defer()
        await self.ensure_voice_state(ctx)
        ctx.voice_state = self.get_voice_state(ctx)

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.send("Pomyślnie dołączyłem na kanał")

    @cog_ext.cog_slash(name='leave', description='Wychodzę z kanału', options=[])
    async def _leave(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.voice_state.voice:
            return await ctx.send('Nie jesteś połączony z żadnym kanałem')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

        await ctx.send("Opuściłem kanał")

    @cog_ext.cog_slash(name='volume', description='Ustawia głośność', options=[
        manage_commands.create_option(
            name='volume',
            description='Wartość głośności',
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def _volume(self, ctx: SlashContext, volume: int):
        await self.ensure_voice_state(ctx)
        ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nic nie gra w tym momencie')
        if 0 > volume > 100:
            return await ctx.send('Wartość musi zawierać się w przedziale 0-100')

        ctx.voice_state.volume = volume / 100

        await ctx.send(f'Głośność została zmieniona na {volume}%')

    @cog_ext.cog_slash(name='now', description='Pokazuje aktualnie graną piosenkę', options=[])
    async def _now(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @cog_ext.cog_slash(name='pause', description='Pauzuje odtwarzacz', options=[])
    async def _pause(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @cog_ext.cog_slash(name='resume', description='Ponawiam odtwarzacz', options=[])
    async def _resume(self, ctx: SlashContext):
        ctx.voice_state = self.get_voice_state(ctx)
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')



    @staticmethod
    async def ensure_voice_state(ctx: SlashContext):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.git ')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')


def setup(bot: PGBot):
    bot.add_cog(Music(bot))
