import requests

from config import API_URL


def announce_join(channel_name: str, user_id: str, username: str) -> None:
  url = f"{API_URL}/channels/{channel_name}/users"
  requests.post(url, json={
    'user_id': user_id,
    'username': username,
  })

def announce_part(channel_name: str, user_id: str) -> None:
  url = f"{API_URL}/channels/{channel_name}/users/{user_id}"
  requests.delete(url)

def announce_color(channel_name: str, user_id: str, color: str) -> None:
  url = f"{API_URL}/channels/{channel_name}/users/{user_id}"
  requests.put(url, json={
    'item_name': color,
  })

def announce_jump(channel_name: str, user_id: str) -> None:
  url = f"{API_URL}/channels/{channel_name}/users/{user_id}/JUMP"
  requests.post(url)
