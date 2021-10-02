from typing import Optional
from . import MemeApi, JbzdMemeApi, KwejkMemeApi
import random


class MemeApiHandler:
    APIS = [JbzdMemeApi, KwejkMemeApi]
    WEBSITES = [api.WEBSITE for api in APIS]

    @staticmethod
    def resolve_api(website: str) -> Optional[MemeApi]:
        for api in MemeApiHandler.APIS:
            if api.WEBSITE == website:
                return api

    @staticmethod
    def random_api() -> MemeApi:
        return random.choice(MemeApiHandler.APIS)
