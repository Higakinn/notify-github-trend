import requests
import os


class Notion:
    def __init__(self):
        self.base_url = "https://api.notion.com/v1/pages"
        token = os.getenv("NOTION_API_TOKEN")
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def create_database(self, database_id: str, notion_properties):
        #
        payload = {
            "parent": {"database_id": database_id},
            "properties": notion_properties,
        }
        response = requests.post(self.base_url, json=payload, headers=self.headers)
        print("post", response.text)
        return response
