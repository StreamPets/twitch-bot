import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

BOT_ID = os.getenv('BOT_ID')
OWNER_ID = os.getenv('OWNER_ID')

LRU_LIMIT = int(os.getenv('LRU_LIMIT', 10))

# BOT_PREFIX = os.getenv('BOT_PREFIX')
