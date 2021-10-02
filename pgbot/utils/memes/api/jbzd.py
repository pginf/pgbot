from pgbot.utils.memes import Meme
from typing import Optional
from pgbot.utils.memes.api import MemeApi
from pgbot.utils.website_utils import WebsiteUtils
from bs4 import BeautifulSoup
import random


class JbzdMemeApi(MemeApi):
    ENDPOINT = "https://jbzd.com.pl/str/"
    WEBSITE = "JBZD"

    @staticmethod
    def scrap(html: str) -> Optional[Meme]:
        soup = BeautifulSoup(html, "html.parser")

        tags = []
        for tag in soup.find_all('a', class_='article-tag'):
            tags.append(tag.text)

        if soup.find('img', class_='article-image'):
            # zdjęcie
            image_url = soup.find('img', class_='article-image')['src']
        elif soup.find('video', class_='video-js'):
            # film
            image_url = soup.find('video', class_='video-js').source['src']

        else:
            return None

        title = soup.find(
            'h3', class_='article-title').a.text.lstrip().rstrip()

        url = soup.find('h3', class_='article-title').a['href']

        meme = Meme(title, url, image_url, tags)

        return meme

    @staticmethod
    async def get() -> Optional[Meme]:
        r_page = random.randint(1, 200)
        url = JbzdMemeApi.ENDPOINT + str(r_page)
        html = await WebsiteUtils.get(url)
        return JbzdMemeApi.scrap(html)
