import asyncio
import logging

import aiohttp
import asyncpg
import twitchio
from twitchio.web import AiohttpAdapter

from app.bot import StreamBot
from app.config import (
    API_URL,
    BOT_ID,
    CLIENT_ID,
    CLIENT_SECRET,
    OWNER_ID,
    PS_USER,
    PS_PASS,
    PS_HOST,
    PS_PORT,
    HOST,
    DOMAIN,
    WEBHOOK_SECRET,
)

LOGGER: logging.Logger = logging.getLogger("Bot")

adapter: AiohttpAdapter = AiohttpAdapter(
    host=HOST,
    domain=DOMAIN,
    eventsub_secret=WEBHOOK_SECRET,
)


def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with (
            asyncpg.create_pool(
                dsn=f"postgres://{PS_USER}:{PS_PASS}@{PS_HOST}:{PS_PORT}/streampets"
            ) as tdb,
            aiohttp.ClientSession(API_URL) as aio_session,
            StreamBot(
                bot_id=BOT_ID,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                owner_id=OWNER_ID,
                token_database=tdb,
                adapter=adapter,
                aio_session=aio_session,
            ) as bot,
        ):
            await bot.setup_database()
            await bot.start()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")


if __name__ == "__main__":
    main()
