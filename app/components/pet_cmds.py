from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import twitchio
from twitchio.ext import commands

from app import api

if TYPE_CHECKING:
    from app.bot import StreamBot

LOGGER: logging.Logger = logging.getLogger("Bot")


class PetComponent(commands.Component):
    def __init__(self, bot: commands.Bot):
        self.bot: StreamBot = bot

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage):
        channel_id = payload.broadcaster.id
        user_id = payload.chatter.id
        username = payload.chatter.name

        if not await self.bot.cache[channel_id].contains(user_id):
            await api.announce_join(
                self.bot.aio_session,
                channel_id,
                user_id,
                username,
            )

        removed_id = await self.bot.cache[channel_id].add_or_update(user_id)
        if removed_id:
            await api.announce_part(
                self.bot.aio_session,
                channel_id,
                removed_id,
            )

    @commands.command(name="jump")
    async def command_jump(self, ctx: commands.Context):
        channel_id = ctx.channel.id
        user_id = ctx.author.id
        await api.announce_jump(
            self.bot.aio_session,
            channel_id,
            user_id,
        )

    @commands.command(name="color", aliases=["colour"])
    async def command_color(self, ctx: commands.Context, color: str):
        channel_id = ctx.channel.id
        user_id = ctx.author.id
        await api.announce_color(
            channel_id,
            user_id,
            color,
        )

    @commands.Component.listener()
    async def event_stream_online(self, payload: twitchio.StreamOnline) -> None:
        await self.bot.join_channel(channel_id=payload.broadcaster.id)

    @commands.Component.listener()
    async def event_stream_offline(self, payload: twitchio.StreamOffline) -> None:
        await self.bot.leave_channel(channel_id=payload.broadcaster.id)


async def setup(bot: commands.Bot):
    await bot.add_component(PetComponent(bot))
