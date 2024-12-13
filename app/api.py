import requests


class ApiService:
  
  def __init__(self, api_url):
    self.api_url = api_url

  def announce_join(self, channel_name: str, user_id: str, username: str) -> None:
    url = f"{self.api_url}/channels/{channel_name}/viewers"
    requests.post(url, json={
      'user_id': user_id,
      'username': username,
    })

  def announce_part(self, channel_name: str, user_id: str) -> None:
    url = f"{self.api_url}/channels/{channel_name}/viewers/{user_id}"
    requests.delete(url)

  def announce_color(self, channel_name: str, user_id: str, color: str) -> None:
    url = f"{self.api_url}/channels/{channel_name}/viewers/{user_id}"
    requests.put(url, json={
      'item_name': color,
    })

  def announce_jump(self, channel_name: str, user_id: str) -> None:
    url = f"{self.api_url}/channels/{channel_name}/viewers/{user_id}/JUMP"
    requests.post(url)
