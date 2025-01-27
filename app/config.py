import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

BOT_ID = os.getenv("BOT_ID")
OWNER_ID = os.getenv("OWNER_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

LRU_LIMIT = int(os.getenv("LRU_LIMIT", 10))

INITIAL_RUN = os.getenv("INITIAL_RUN") == "True"

PS_USER = os.getenv("PS_USER")
PS_PASS = os.getenv("PS_PASS")
PS_HOST = os.getenv("PS_HOST")
PS_PORT = os.getenv("PS_PORT")

HOST = os.getenv("HOST")
DOMAIN = os.getenv("DOMAIN")
