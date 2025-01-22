import asyncio
import twitchio
from twitchio.ext import commands, eventsub

from .bot import ChatBot

from app.config import (
  BOT_TOKEN,
  BOT_PREFIX,
  WEBHOOK_SECRET,
)


channel_name = "ljrexcodes"
channel_id = 83125762

bots: dict[str, ChatBot] = {}
lock = asyncio.Lock()

class Orchastrator(commands.Bot):
  
  def __init__(self, token, prefix):
    super().__init__(token=token, prefix=prefix)

  async def __ainit__(self):
    try:
      await esclient.subscribe_channel_stream_start(channel_id)
      await esclient.subscribe_channel_stream_end(channel_id)
    except twitchio.HTTPException:
      pass

orchastrator = Orchastrator(BOT_TOKEN, BOT_PREFIX)
orchastrator.loop.run_until_complete(orchastrator.__ainit__())

esclient = eventsub.EventSubClient(
  orchastrator,
  webhook_secret=WEBHOOK_SECRET,
  callback_route='bot.streampets.io',
)

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
