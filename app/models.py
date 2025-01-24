import asyncio
import time


class LruCache:

  def __init__(self, limit) -> None:
    self.timestamps: dict[str,float] = {}
    self.limit = limit
    self.lock = asyncio.Lock()

  async def keys(self):
    async with self.lock:
      return list(self.timestamps.keys())

  async def add_or_update(self, user_id: str) -> str | None:
    '''Returns the id of the removed user, or None if no user was removed.'''
    async with self.lock:

      timestamp = time.time()
      self.timestamps[user_id] = timestamp

      if len(self.timestamps) <= self.limit:
        return None
      
      min_id, min_ts = user_id, timestamp
      for id, ts in self.timestamps.items():
        if ts < min_ts:
          min_id, min_ts = id, ts

      del self.timestamps[min_id]
      return min_id

  async def contains(self, user_id: str) -> bool:
    async with self.lock:
      return user_id in self.timestamps
