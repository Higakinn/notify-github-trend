import os
import time

import jinja2

from lib.notion_client import Notion
from exactractor import github
from notifier.qiita import Qiita


def main():
    program_languages = os.getenv("PROGRAM_LANGUAGES").split(",")
    notion_database_id = os.getenv("NOTION_DATABAE_ID")
    article_ids = os.getenv("ARTICLE_IDS").split(",")
    notion_client = Notion()
    all_languages_trends = github.fetch_trends()
    for trend in all_languages_trends:
        print(trend)
        notion_properties = {
            "repo_name": {"title": [{"text": {"content": trend["title"]}}]},
            "language": {"multi_select": [{"name": trend["language"]}]},
            "url": {"url": trend["url"]},
            "description": {"rich_text": [{"text": {"content": trend["description"]}}]},
            "description_ja": {
                "rich_text": [{"text": {"content": trend["description_ja"]}}]
            },
            "star": {"rich_text": [{"text": {"content": trend["star"]}}]},
        }
        notion_client.create_database(
            database_id=notion_database_id, notion_properties=notion_properties
        )
        time.sleep(0.5)

    for program_language, article_id in zip(program_languages, article_ids):
        rs = github.get_trends(language=program_language)
        # NOTE: markdown 組み立て
        fileSystemLoader = jinja2.FileSystemLoader(
            searchpath=f"{os.getcwd()}/notify_ghtrend/resource"
        )
        env = jinja2.Environment(loader=fileSystemLoader)
        template = env.get_template("test.tpl")
        md_content = template.render({"language": program_language, "repos": rs})

        # NOTE: 外部サービスにpost
        title = f"{program_language} GitHubトレンドデイリーランキング!!【自動更新】"
        # Qiita().post(program_language, title, md_content)
        Qiita().update(program_language, title, md_content, article_id)
        time.sleep(1.5)


if __name__ == "__main__":
    main()
