from .api import ApiService
from .bot import ChatBot
from .config import API_URL

api_service = ApiService(API_URL)
chat_bot = ChatBot(api_service)
