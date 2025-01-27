import asyncio
import time


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
