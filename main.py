import asyncio
import logging

import aiohttp
import asyncpg
import twitchio

from app.utils import MyAiohttpAdapter
from app.bot import StreamBot
from app.config import (
    API_URL,
    BOT_ID,
    CLIENT_ID,
    CLIENT_SECRET,
    DOMAIN,
    HOST,
    OWNER_ID,
    PS_HOST,
    PS_NAME,
    PS_PASS,
    PS_PORT,
    PS_USER,
    WEBHOOK_SECRET,
    OAUTH_REDIRECT_URL,
)

LOGGER: logging.Logger = logging.getLogger("Bot")


adapter = MyAiohttpAdapter(
    host=HOST,
    domain=DOMAIN,
    eventsub_secret=WEBHOOK_SECRET,
    oauth_redirect_url=OAUTH_REDIRECT_URL,
)


def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with (
            asyncpg.create_pool(
                dsn=f"postgres://{PS_USER}:{PS_PASS}@{PS_HOST}:{PS_PORT}/{PS_NAME}"
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
