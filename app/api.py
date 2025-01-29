import logging

import aiohttp

LOGGER: logging.Logger = logging.getLogger(__name__)


async def announce_join(
    session: aiohttp.ClientSession,
    channel_id: str,
    user_id: str,
    username: str,
) -> None:
    url = f"/channels/{channel_id}/users"
    async with session.post(
        url,
        json={
            "user_id": user_id,
            "username": username,
        },
    ) as response:
        if response.status != 204:
            LOGGER.error("received status code %d from announce join", response.status)


async def announce_part(
    session: aiohttp.ClientSession,
    channel_id: str,
    user_id: str,
) -> None:
    url = f"/channels/{channel_id}/users/{user_id}"
    async with session.delete(url) as response:
        if response.status != 204:
            LOGGER.error("received status code %d from announce part", response.status)


async def announce_color(
    session: aiohttp.ClientSession,
    channel_id: str,
    user_id: str,
    color: str,
) -> None:
    url = f"/channels/{channel_id}/users/{user_id}"
    async with session.put(
        url,
        json={"item_name": color},
    ) as response:
        if response.status != 204:
            LOGGER.error("received status code %d from announce color", response.status)


async def announce_jump(
    session: aiohttp.ClientSession,
    channel_id: str,
    user_id: str,
) -> None:
    url = f"/channels/{channel_id}/users/{user_id}/JUMP"
    async with session.post(url) as response:
        if response.status != 204:
            LOGGER.error("received status code %d from announce jump", response.status)
