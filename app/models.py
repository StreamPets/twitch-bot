from dataclasses import dataclass
from typing import Optional


@dataclass
class Color:
  id: int
  name: str
  img: str
  sku: str
  prev: str

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'img': self.img,
      'sku': self.sku,
      'prev': self.prev,
    }


@dataclass
class Viewer:
  user_id: str
  username: Optional[str] = None
  color: Optional[Color] = None

  def __eq__(self, other: object) -> bool:
    if isinstance(other, Viewer):
      return self.user_id == other.user_id
    return False

  def to_dict(self):
    return {
      'userID': self.user_id,
      'username': self.username,
      'color': self.color.to_dict(),
    }
