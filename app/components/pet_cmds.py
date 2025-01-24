import twitchio
from twitchio import eventsub
from twitchio.ext import commands

from app import api
from app.config import (
  LRU_LIMIT,
)
from app.models import LruCache


class PetComponent(commands.Component):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.cache: dict[str,LruCache] = {}
    self.sub_maps: dict[str,str] = {}

  @commands.Component.listener()
  async def event_message(self, payload: twitchio.ChatMessage):
    channel_name = payload.broadcaster.name
    user_id = payload.chatter.id
    username = payload.chatter.name

    print(payload.text)

    if not await self.cache.contains(user_id):
      api.announce_join(channel_name, user_id, username)

    removed_id = await self.cache.add_or_update(user_id)
    if removed_id:
      api.announce_part(channel_name, removed_id)

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

  @commands.Component.listener()
  async def event_stream_online(self, payload: twitchio.StreamOnline) -> None:
    channel_id = payload.broadcaster.id
    self.cache[channel_id] = LruCache[LRU_LIMIT]

    subscription = eventsub.ChatMessageSubscription(broadcaster_user_id=channel_id, user_id=self.bot.bot_id)
    sub = await self.bot.subscribe_websocket(payload=subscription)

    self.sub_maps[channel_id] = sub["data"][0]["id"]

  @commands.Component.listener()
  async def event_stream_offline(self, payload: twitchio.StreamOffline) -> None:
    channel_id = payload.broadcaster.id
    await self.bot.delete_eventsub_subscription(self.sub_maps[channel_id])

    for user_id in await self.cache[channel_id].keys():
      api.announce_part(payload.broadcaster.name, user_id)

    self.cache.pop(channel_id)

async def setup(bot: commands.Bot):
  await bot.add_component(PetComponent(bot))
