import os
import requests

LINE_API_URL = "https://api.line.me/v2/bot/message/push"


def push_message(text: str) -> None:
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    body = {
        "to": user_id,
        "messages": [{"type": "text", "text": text}],
    }

    res = requests.post(LINE_API_URL, headers=headers, json=body)
    res.raise_for_status()
