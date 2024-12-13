import time
from typing import Optional


class NotInLruException(KeyError):
  pass

class UserLru:

  def __init__(self, limit) -> None:
    self.timestamps: dict[str,float] = {}
    self.limit = limit

  def add(self, user_id: str) -> Optional[str]:
    '''Returns the id of the removed user, or None if no user was removed.'''
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

  def update_user(self, user_id: str) -> float:
    '''Updates the user's timestamp to the current time.
    Raises an exception if user_id not already present.'''
    if user_id not in self.timestamps:
      raise NotInLruException(f"The user id {user_id} was not present")
    self.timestamps[user_id] = time.time()
    return self.timestamps[user_id]

  def __contains__(self, user_id: str) -> bool:
    return user_id in self.timestamps
