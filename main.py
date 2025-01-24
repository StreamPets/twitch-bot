import asyncio
import logging

import asqlite
import twitchio

from app.bot import StreamBot

from app.config import (
  BOT_ID,
  CLIENT_ID,
  CLIENT_SECRET,
  OWNER_ID,
)


LOGGER: logging.Logger = logging.getLogger("Bot")

channel_id = '429166219'


def main() -> None:
  twitchio.utils.setup_logging(level=logging.INFO)

  async def runner() -> None:
    async with asqlite.create_pool("tokens.db") as tdb, StreamBot(
      bot_id=BOT_ID,
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      owner_id=OWNER_ID,
      token_database=tdb,
    ) as bot:
      await bot.setup_database()
      await bot.add_channel(channel_id)
      await bot.start()

  try:
    asyncio.run(runner())
  except KeyboardInterrupt:
    LOGGER.warning("Shutting down due to KeyboardInterrupt...")

if __name__ == '__main__':
  main()
