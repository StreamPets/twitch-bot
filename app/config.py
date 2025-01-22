import os
import secrets

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')

LRU_LIMIT = int(os.getenv('LRU_LIMIT', 10))

BOT_NAMES = os.getenv('BOT_NAMES').split(',')
BOT_PREFIX = os.getenv('BOT_PREFIX')

WEBHOOK_SECRET = secret = secrets.token_hex(16)
print(WEBHOOK_SECRET)
