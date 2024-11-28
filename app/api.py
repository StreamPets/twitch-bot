from urllib.parse import urlparse
import requests


class ApiService:
  
  def __init__(self, api_url):
    self.api_url = api_url

  def announce_join(self, channel_name: str, user_id: str, username: str) -> None:
    url = urlparse(self.api_url, "join")
    requests.post(url, {
      'channel_name': channel_name,
      'user_id': user_id,
      'username': username,
    })

  def announce_part(self, channel_name: str, user_id: str) -> None:
    url = urlparse(self.api_url, "part")
    requests.delete(url, {
      'channel_name': channel_name,
      'user_id': user_id,
    })

  def announce_color(self, channel_name: str, user_id: str, color: str) -> None:
    url = urlparse(self.api_url, "color")
    requests.put(url, {
      'channel_name': channel_name,
      'user_id': user_id,
      'color': color,
    })

  def announce_jump(self, channel_name: str, user_id: str) -> None:
    url = urlparse(self.api_url, "action")
    requests.post(url, {
      'channel_name': channel_name,
      'user_id': user_id,
      'action': 'jump'
    })
