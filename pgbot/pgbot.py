import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from pathlib import Path
from pgbot.db.session import session


class PGBot(commands.Bot):
    def __init__(self, token: str):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            reconnect=True,
        )

        self.token = token
        self.MAIN_PATH: Path = Path("pgbot")

    def run(self):
        try:
            self.loop.run_until_complete(self.bot_start())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.bot_stop())

    def load_extensions(self, path: Path):
        if not path.is_dir() and not path.exists():
            return

        extensions = [ext for ext in path.iterdir() if ext.suffix == ".py"]
        for extension in extensions:
            extension_path = ".".join(extension.with_suffix("").parts)
            try:
                self.load_extension(extension_path)
                print(f"LOADED {extension_path}")
            except Exception as e:
                print(f"FAILED {extension_path}")
                print(e)

    async def bot_start(self):
        slash = SlashCommand(self, override_type=True, sync_commands=True)

        self.load_extensions(self.MAIN_PATH.joinpath("commands"))
        self.load_extensions(self.MAIN_PATH.joinpath("tasks"))
        self.load_extensions(self.MAIN_PATH.joinpath("events"))

        await self.login(self.token)
        await self.connect()

    async def bot_stop(self):
        await super().close()
        session.close()

    async def on_ready(self):
        print(
            f'\nZalogowano jako : {self.user} - {self.user.id}\n')
