import asyncio
import twitchio
from twitchio.ext import commands, eventsub

from .bot import ChatBot

from app.config import (
  CLIENT_ID,
  CLIENT_SECRET,
  WEBHOOK_SECRET,
)


channel_name = "ljrexcodes"
channel_id = 83125762

bots: dict[str, ChatBot] = {}
lock = asyncio.Lock()

esbot = commands.Bot.from_client_credentials(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
)

esclient = eventsub.EventSubClient(
  esbot,
  webhook_secret=WEBHOOK_SECRET,
  callback_route='https://bot.streampets.io',
)

async def __ainit__():
  await esclient.subscribe_channel_stream_start(channel_id)
  await esclient.subscribe_channel_stream_end(channel_id)

esbot.loop.run_until_complete(__ainit__())

@esbot.event()
async def subscribe_channel_stream_start(payload: eventsub.StreamOnlineData):
  print("Stream started")
  channel_id = payload.broadcaster.id
  chat_bot = ChatBot(esclient, channel_id)
  esbot.loop.create_task(chat_bot.start())
  async with lock:
    bots[channel_id] = chat_bot

@esbot.event()
async def subscribe_channel_stream_end(payload: eventsub.StreamOfflineData):
  print("Stream ended")
  async with lock:
    await bots[payload.broadcaster.id].del_async()
    del bots[payload.broadcaster.id]

esbot.loop.create_task(esclient.listen(port=4000))
esbot.loop.create_task(esbot.start())
