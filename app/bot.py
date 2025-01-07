from twitchio.ext import commands

from app.api import ApiService
from app.models import UserLru

from app.config import (
  BOT_NAMES,
  BOT_PREFIX,
  BOT_TOKEN,
  LRU_LIMIT,
)

class ChatBot(commands.Bot):
  def __init__(self, api: ApiService):
    super().__init__(
      token=BOT_TOKEN,
      prefix=BOT_PREFIX,
      initial_channels=["ljrexcodes"],
    )
    self.api = api

    self.lru: dict[str,UserLru] = {}

    self.load_module("app.commands")

  async def event_message(self, message):
    if not message.author or message.author.name in BOT_NAMES:
      return
    
    channel_name = message.channel.name
    user_id = message.author.id
    username = message.author.name

    if channel_name not in self.lru:
      self.lru[channel_name] = UserLru(LRU_LIMIT)

    if user_id in self.lru[channel_name]:
      self.lru[channel_name].update_user(user_id)
    else:
      self.api.announce_join(channel_name, user_id, username)
      removed_id = self.lru[channel_name].add(user_id)
      if removed_id:
        self.api.announce_part(channel_name, removed_id)

    await self.handle_commands(message)
