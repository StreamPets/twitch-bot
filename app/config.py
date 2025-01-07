import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')

LRU_LIMIT = 25

BOT_NAMES = ['rexxauto', 'streamelements']
BOT_PREFIX = '!'
