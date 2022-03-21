import os
import requests
import json
from .base import Base

class Qiita(Base):
  def post(self, lang, title, md_file):
      api_base_url = "https://qiita.com/"
      post_api_url = f"{api_base_url}api/v2/items"
      access_token = os.getenv("QIITA_API_TOKEN")
      headers = {
        "Authorization": f"Bearer {access_token}"
      }
      with open(f'{os.getcwd()}/notify_ghtrend/resource/sample.json') as f:
        item_data = json.loads(f.read())

      item_data['title'] = title
      item_data['body'] = md_file
      item_data['tags'][0]["name"] = lang
      print(item_data)
      result = requests.post(
        post_api_url, 
        headers=headers, 
        json=item_data
      )

      print(result.json())