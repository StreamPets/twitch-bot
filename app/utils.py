import asyncio
import logging
import time

from aiohttp import web
from twitchio.web import AiohttpAdapter

LOGGER: logging.Logger = logging.getLogger("Bot")


class MyAiohttpAdapter(AiohttpAdapter):
    def __init__(
        self,
        *,
        host=None,
        port=None,
        domain=None,
        eventsub_path=None,
        eventsub_secret=None,
        oauth_redirect_url=None,
        cookie_domain=None,
    ):
        super().__init__(
            host=host,
            port=port,
            domain=domain,
            eventsub_path=eventsub_path,
            eventsub_secret=eventsub_secret,
        )

        self.__oauth_redirect_url = oauth_redirect_url
        self.__cookie_domain = cookie_domain

    async def fetch_token(self, request):
        if "code" not in request.query:
            return web.Response(status=400)

        try:
            payload = await self.client._http.user_access_token(
                request.query["code"],
                redirect_uri=self.redirect_url,
            )
        except Exception as e:
            LOGGER.error(
                "Exception raised while fetching Token in <%s>: %s",
                self.__class__.__qualname__,
                e,
            )
            return web.Response(status=500)

        self.client.dispatch(event="oauth_authorized", payload=payload)
        response = web.HTTPPermanentRedirect(
            location=self.__oauth_redirect_url,
        )
        response.set_cookie(
            "different-cookie-name",
            payload.access_token,
            domain=self.__cookie_domain,
            httponly=True,
            secure=True,
        )
        return response


class ViewerCache:
    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.timestamps: dict[str, float] = {}
        self.lock = asyncio.Lock()

    async def user_ids(self) -> list[str]:
        """Returns a list of the user ids stored in the cache."""
        async with self.lock:
            return list(self.timestamps.keys())

    async def add_or_update(self, user_id: str) -> str | None:
        """Returns the id of the removed user, or None if no user was removed."""
        async with self.lock:
            timestamp = time.time()
            self.timestamps[user_id] = timestamp

            if len(self.timestamps) <= self.limit:
                return None

            min_id, min_ts = user_id, timestamp
            for id, ts in self.timestamps.items():
                if ts < min_ts:
                    min_id, min_ts = id, ts

            self.timestamps.pop(min_id)
            return min_id

    async def contains(self, user_id: str) -> bool:
        """Returns True if the user_id is in the cache, or False otherwise."""
        async with self.lock:
            return user_id in self.timestamps
