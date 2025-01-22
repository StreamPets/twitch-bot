import asyncio
import twitchio
from twitchio.ext import commands, eventsub

from .bot import ChatBot

from app.config import (
  BOT_TOKEN,
  WEBHOOK_SECRET,
)


channel_name = "ljrexcodes"
channel_id = 83125762

bots: dict[str, ChatBot] = {}
lock = asyncio.Lock()

orchastrator = commands.Bot(BOT_TOKEN)

esclient = eventsub.EventSubClient(
  orchastrator,
  webhook_secret=WEBHOOK_SECRET,
  callback_route='bot.streampets.io',
)

async def __ainit__():
  try:
    await esclient.subscribe_channel_stream_start(channel_id)
    await esclient.subscribe_channel_stream_end(channel_id)
  except twitchio.HTTPException:
    pass

orchastrator.loop.run_until_complete(__ainit__())

@orchastrator.event()
async def subscribe_channel_stream_start(payload: eventsub.StreamOnlineData):
  print("Stream started")
  channel_id = payload.broadcaster.id
  chat_bot = ChatBot(esclient, channel_id)
  orchastrator.loop.create_task(chat_bot.start())
  async with lock:
    bots[channel_id] = chat_bot

@orchastrator.event()
async def subscribe_channel_stream_end(payload: eventsub.StreamOfflineData):
  print("Stream ended")
  async with lock:
    await bots[payload.broadcaster.id].del_async()
    del bots[payload.broadcaster.id]

orchastrator.loop.create_task(esclient.listen(port=4000))
orchastrator.loop.create_task(orchastrator.start())
