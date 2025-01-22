import aiorwlock
from twitchio.ext import commands, eventsub

from app import api
from app.models import LruCache

from app.config import (
  BOT_NAMES,
  LRU_LIMIT,
)


class ChatBot(commands.Bot):

  def __init__(self, token, prefix, channel_id, channel_name, esclient: eventsub.EventSubClient):
    super().__init__(
      token=token,
      prefix=prefix,
      initial_channels=[channel_name],
    )

    self.esclient = esclient
    self.cache = LruCache(LRU_LIMIT)
    self.channel_id = channel_id
    self.channel_name = channel_name
    self.closing = False
    self.lock = aiorwlock.RWLock()

    self.load_module("app.commands")

  async def del_async(self):
    async with self.lock.writer_lock:
      self.closing = True
      for user_id in await self.cache.keys():
        api.announce_part(self.channel_name, user_id)

  async def event_message(self, message):
    async with self.lock.reader_lock:
      if self.closing:
        return

      if not message.author or message.author.name in BOT_NAMES:
        return

      channel_name = message.channel.name
      user_id = message.author.id
      username = message.author.name

      if not await self.cache.contains(user_id):
        api.announce_join(channel_name, user_id, username)

      removed_id = await self.cache.add_or_update(user_id)
      if removed_id:
        api.announce_part(channel_name, removed_id)

      await self.handle_commands(message)

  @commands.command(name='jump')
  async def command_jump(self, ctx: commands.Context):
    channel_name = ctx.channel.name
    user_id = ctx.author.id
    api.announce_jump(channel_name, user_id)

  @commands.command(name='color', aliases=['colour'])
  async def command_color(self, ctx: commands.Context, color: str):
    channel_name = ctx.channel.name
    user_id = ctx.author.id
    api.announce_color(channel_name, user_id, color)

  @commands.command(name='discord')
  async def command_discord(self, ctx: commands.Context):
    await ctx.send("https://discord.gg/S2MDMqk")
