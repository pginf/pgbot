import os
import dotenv
from pgbot import PGBot

if __name__ == "__main__":
    dotenv.load_dotenv()

    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        raise("Could not load token from env")

    pgbot = PGBot(TOKEN)
    pgbot.run()
