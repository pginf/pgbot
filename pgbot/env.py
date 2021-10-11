import os
import dotenv
dotenv.load_dotenv()

DEBUG = os.environ.get("DEBUG") == "true"

TOKEN = ""
if DEBUG:
    TOKEN = os.environ.get("DEBUG_TOKEN")
else:
    TOKEN = os.environ.get("TOKEN")

DATABASE_URL = ""
if DEBUG:
    DATABASE_URL = os.environ.get("DEBUG_DATABASE_URL")
else:
    DATABASE_URL = os.environ.get("DATABASE_URL")
