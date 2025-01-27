from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import twitchio
from twitchio import eventsub
from twitchio.ext import commands

from app import api
from app.models import ViewerCache
from app.config import (
    LRU_LIMIT,
)

if TYPE_CHECKING:
    from app.bot import StreamBot

LOGGER: logging.Logger = logging.getLogger("Bot")


class PetComponent(commands.Component):
    def __init__(self, bot: commands.Bot):
        self.bot: StreamBot = bot
        self.cache: dict[str, ViewerCache] = {}
        self.sub_maps: dict[str, str] = {}

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage):
        channel_name = payload.broadcaster.name
        channel_id = payload.broadcaster.id
        user_id = payload.chatter.id
        username = payload.chatter.name

        if not await self.cache[channel_id].contains(user_id):
            await api.announce_join(
                self.bot.aio_session,
                channel_name,
                user_id,
                username,
            )

        removed_id = await self.cache[channel_id].add_or_update(user_id)
        if removed_id:
            await api.announce_part(
                self.bot.aio_session,
                channel_name,
                removed_id,
            )

    @commands.command(name="jump")
    async def command_jump(self, ctx: commands.Context):
        channel_name = ctx.channel.name
        user_id = ctx.author.id
        await api.announce_jump(
            self.bot.aio_session,
            channel_name,
            user_id,
        )

    @commands.command(name="color", aliases=["colour"])
    async def command_color(self, ctx: commands.Context, color: str):
        channel_name = ctx.channel.name
        user_id = ctx.author.id
        await api.announce_color(
            channel_name,
            user_id,
            color,
        )

    @commands.Component.listener()
    async def event_stream_online(self, payload: twitchio.StreamOnline) -> None:
        channel_id = payload.broadcaster.id
        LOGGER.info("joining channel %s...", channel_id)

        self.cache[channel_id] = ViewerCache(LRU_LIMIT)

        subscription = eventsub.ChatMessageSubscription(
            broadcaster_user_id=channel_id,
            user_id=self.bot.bot_id,
        )
        sub = await self.bot.subscribe_websocket(payload=subscription, as_bot=True)

        self.sub_maps[channel_id] = sub["data"][0]["id"]
        LOGGER.info("joined channel %s", channel_id)

    @commands.Component.listener()
    async def event_stream_offline(self, payload: twitchio.StreamOffline) -> None:
        channel_id = payload.broadcaster.id
        channel_name = payload.broadcaster.id
        LOGGER.info("leaving channel %s...", channel_id)

        if channel_id not in self.sub_maps:
            LOGGER.error("failed to leave channel %s: bot not in channel", channel_id)
            return

        await self.bot.delete_eventsub_subscription(
            self.sub_maps[channel_id],
            token_for=self.bot.bot_id,
        )

        for user_id in await self.cache[channel_id].user_ids():
            await api.announce_part(
                self.bot.aio_session,
                channel_name,
                user_id,
            )

        self.cache.pop(channel_id)
        LOGGER.info("leaving channel %s successful", channel_id)


async def setup(bot: commands.Bot):
    await bot.add_component(PetComponent(bot))
