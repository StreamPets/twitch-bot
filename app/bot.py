import logging

import aiohttp
import asyncpg
import twitchio
from twitchio.ext import commands
from twitchio import eventsub, web

from app.config import (
    CHANNEL_ID,
    INITIAL_RUN,
)

LOGGER: logging.Logger = logging.getLogger("Bot")


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

        LOGGER.info("INTIAL_RUN = %s", INITIAL_RUN)
        if not INITIAL_RUN:
            await self.add_channel(CHANNEL_ID)

    async def add_token(
        self, token: str, refresh: str
    ) -> twitchio.authentication.ValidateTokenPayload:
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(
            token, refresh
        )

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
        async with self.token_database.acquire() as connection:
            rows: list[asyncpg.Record] = await connection.fetch(
                """SELECT * from tokens"""
            )

        for row in rows:
            await self.add_token(row["token"], row["refresh"])

    async def setup_database(self) -> None:
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        async with self.token_database.acquire() as connection:
            await connection.execute(query)

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)

    async def add_channel(self, channel_id: str) -> None:
        sub = eventsub.StreamOnlineSubscription(broadcaster_user_id=channel_id)
        await self.subscribe_websocket(payload=sub)
        LOGGER.info("listening to online events for %s", channel_id)

        sub = eventsub.StreamOfflineSubscription(broadcaster_user_id=channel_id)
        await self.subscribe_websocket(payload=sub)
        LOGGER.info("listening to offline events for %s", channel_id)
