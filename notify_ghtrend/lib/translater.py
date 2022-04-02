import os
import requests


def translate(text: str, source: str = "", target="ja"):
    url = os.getenv("TRANSLATE_API_URL")
    headers = {"content-type": "application/json"}
    item_data = {"text": text, "source": source, "target": target}
    res = requests.post(url, headers=headers, json=item_data)
    return res.json()
