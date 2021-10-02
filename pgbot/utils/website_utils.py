import aiohttp
import io


class WebsiteUtils:
    @staticmethod
    async def get(url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = io.BytesIO(await resp.read())
                return data
