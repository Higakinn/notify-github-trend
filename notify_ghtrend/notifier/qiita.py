import os
import requests
import json
from .base import Base


class Qiita(Base):
    def __init__(self) -> None:
        self.api_base_url = "https://qiita.com/"
        self.access_token = os.getenv("QIITA_API_TOKEN")

    def post(self, lang, title, md_file):
        post_api_url = f"{self.api_base_url}api/v2/items"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        with open(
            f"{os.getcwd()}/notify_ghtrend/resource/qiita_request_body.json"
        ) as f:
            item_data = json.loads(f.read())

        item_data["title"] = title
        item_data["body"] = md_file
        item_data["tags"][0]["name"] = lang

        result = requests.post(post_api_url, headers=headers, json=item_data)

        print(result.json())

    def update(self, lang, title, md_file, article_id):
        patch_api_url = f"{self.api_base_url}api/v2/items/{article_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        with open(
            f"{os.getcwd()}/notify_ghtrend/resource/qiita_request_body.json"
        ) as f:
            item_data = json.loads(f.read())

        item_data["title"] = title
        item_data["body"] = md_file
        item_data["tags"][0]["name"] = lang

        result = requests.patch(patch_api_url, headers=headers, json=item_data)

        print(result.json())
