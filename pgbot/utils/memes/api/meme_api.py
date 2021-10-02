from typing import Optional
from pgbot.utils.memes import Meme


class MemeApi:
    ENDPOINT = ""
    WEBSITE = ""

    @staticmethod
    def scrap(html: str) -> Optional[Meme]:
        pass

    @staticmethod
    async def get() -> Meme:
        pass
