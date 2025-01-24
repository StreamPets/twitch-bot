import aiohttp

from app.config import API_URL


async def announce_join(
    session: aiohttp.ClientSession,
    channel_name: str,
    user_id: str,
    username: str,
) -> None:
    url = f"{API_URL}/channels/{channel_name}/users"
    async with session.post(
        url,
        json={
            "user_id": user_id,
            "username": username,
        },
    ) as response:
        await response.json()


async def announce_part(
    session: aiohttp.ClientSession,
    channel_name: str,
    user_id: str,
) -> None:
    url = f"{API_URL}/channels/{channel_name}/users/{user_id}"
    async with session.delete(url) as response:
        await response.json()


async def announce_color(
    session: aiohttp.ClientSession,
    channel_name: str,
    user_id: str,
    color: str,
) -> None:
    url = f"{API_URL}/channels/{channel_name}/users/{user_id}"
    async with session.put(
        url,
        json={"item_name": color},
    ) as response:
        await response.json()


async def announce_jump(
    session: aiohttp.ClientSession,
    channel_name: str,
    user_id: str,
) -> None:
    url = f"{API_URL}/channels/{channel_name}/users/{user_id}/JUMP"
    async with session.post(url) as response:
        await response.json()
