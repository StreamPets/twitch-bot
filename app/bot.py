import logging

import aiohttp
import asyncpg
import twitchio
from twitchio.ext import commands
from twitchio import eventsub, web

from app.config import INITIAL_RUN

LOGGER: logging.Logger = logging.getLogger("Bot")

channel_id = "429166219"


class StreamBot(commands.Bot):
    def __init__(
        self,
        *,
        bot_id: str,
        client_id: str,
        client_secret: str,
        owner_id: str,
        token_database: asyncpg.Pool,
        adapter: web.AiohttpAdapter,
        aio_session: aiohttp.ClientSession,
    ) -> None:
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            bot_id=bot_id,
            owner_id=owner_id,
            prefix="!",
            adapter=adapter,
        )

        self.aio_session = aio_session
        self.token_database = token_database

    async def setup_hook(self) -> None:
        await self.load_module("app.components.pet_cmds")
        await self.load_module("app.components.social_cmds")

        if not INITIAL_RUN:
            await self.add_channel(channel_id)

    async def add_token(
        self, token: str, refresh: str
    ) -> twitchio.authentication.ValidateTokenPayload:
        # Make sure to call super() as it will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(
            token, refresh
        )

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
    INSERT INTO tokens (user_id, token, refresh)
    VALUES ($1, $2, $3)
    ON CONFLICT (user_id)
    DO UPDATE SET
        token = EXCLUDED.token,
        refresh = EXCLUDED.refresh;
    """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, resp.user_id, token, refresh)

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def load_tokens(self, path: str | None = None) -> None:
        # We don't need to call this manually, it is called in .login() from .start() internally...

        async with self.token_database.acquire() as connection:
            rows: list[asyncpg.Record] = await connection.fetch(
                """SELECT * from tokens"""
            )

        for row in rows:
            await self.add_token(row["token"], row["refresh"])

    async def setup_database(self) -> None:
        # Create our token table, if it doesn't exist..
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        async with self.token_database.acquire() as connection:
            await connection.execute(query)

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)

    async def add_channel(self, channel_id) -> None:
        subscription = eventsub.StreamOnlineSubscription(broadcaster_user_id=channel_id)
        await self.subscribe_websocket(payload=subscription)

        subscription = eventsub.StreamOfflineSubscription(
            broadcaster_user_id=channel_id
        )
        await self.subscribe_websocket(payload=subscription)
