import logging

import aiohttp
import asyncpg
import twitchio
from twitchio.ext import commands
from twitchio import eventsub, web

from app import api
from app.models import ViewerCache
from app.config import (
    INITIAL_RUN,
    LRU_LIMIT,
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

        self.cache: dict[str, ViewerCache] = {}
        self.sub_maps: dict[str, str] = {}

    async def setup_hook(self) -> None:
        await self.load_module("app.components.pet_cmds")
        await self.load_module("app.components.social_cmds")

        LOGGER.info("INTIAL_RUN = %s", INITIAL_RUN)
        if INITIAL_RUN:
            return

        async with self.token_database.acquire() as connection:
            rows: list[asyncpg.Record] = await connection.fetch(
                """SELECT * FROM channels"""
            )

        for row in rows:
            channel_id = row["channel_id"]
            await self.subscribe_online_events(channel_id)
            await self.subscribe_offline_events(channel_id)
            async for stream in self.fetch_streams(user_ids=[channel_id]):
                if stream.type == "live":
                    await self.join_channel(channel_id)
                    break

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

    async def subscribe_online_events(self, channel_id: str) -> None:
        sub = eventsub.StreamOnlineSubscription(broadcaster_user_id=channel_id)
        await self.subscribe_websocket(payload=sub)
        LOGGER.info("listening to online events for %s", channel_id)

    async def subscribe_offline_events(self, channel_id: str) -> None:
        sub = eventsub.StreamOfflineSubscription(broadcaster_user_id=channel_id)
        await self.subscribe_websocket(payload=sub)
        LOGGER.info("listening to offline events for %s", channel_id)

    async def join_channel(self, channel_id: str) -> None:
        LOGGER.info("joining channel %s...", channel_id)

        self.cache[channel_id] = ViewerCache(LRU_LIMIT)

        subscription = eventsub.ChatMessageSubscription(
            broadcaster_user_id=channel_id,
            user_id=self.bot_id,
        )
        sub = await self.subscribe_websocket(payload=subscription, as_bot=True)

        if not sub:
            return

        self.sub_maps[channel_id] = sub["data"][0]["id"]
        LOGGER.info("joined channel %s", channel_id)

    async def leave_channel(self, channel_id: str) -> None:
        LOGGER.info("leaving channel %s...", channel_id)

        if channel_id not in self.sub_maps:
            LOGGER.error("failed to leave channel %s: bot not in channel", channel_id)
            return

        await self.delete_eventsub_subscription(
            self.sub_maps[channel_id],
            token_for=self.bot_id,
        )

        for user_id in await self.cache[channel_id].user_ids():
            await api.announce_part(
                self.aio_session,
                channel_id,
                user_id,
            )

        self.cache.pop(channel_id)
        LOGGER.info("leaving channel %s successful", channel_id)
