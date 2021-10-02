from typing import Optional

from bs4 import BeautifulSoup

from pgbot.utils.memes import Meme
from pgbot.utils.memes.api import MemeApi
from pgbot.utils.website_utils import WebsiteUtils


class KwejkMemeApi(MemeApi):
    ENDPOINT = "https://kwejk.pl/losowy"
    WEBSITE = "Kwejk"

    @staticmethod
    def scrap(html: str) -> Optional[Meme]:
        soup = BeautifulSoup(html, 'html.parser')

        url_div = soup.find('div', class_='fb-like')
        if url_div:
            url = url_div.get('data-href')
        else:
            return None

        full_img = soup.find('img', class_='full-image')
        if full_img:
            image_url = full_img.get('src')
            title = full_img.get('alt')
        else:
            return None

        tags = []

        tag_list = soup.find('div', class_='tag-list')

        if not tag_list:
            return None

        for tag in tag_list.find_all('a'):
            tags.append(tag.text)

        meme = Meme(title, url, image_url, tags)
        return meme

    @staticmethod
    async def get() -> Optional[Meme]:
        url = KwejkMemeApi.ENDPOINT

        # Kwejk czasem ma problemy dlatego proby
        html = await WebsiteUtils.get(url)
        meme = KwejkMemeApi.scrap(html)

        tries = 5
        while not meme:
            html = await WebsiteUtils.get(url)
            meme = KwejkMemeApi.scrap(html)
            tries -= 1

            if tries <= 0:
                break

        return meme
