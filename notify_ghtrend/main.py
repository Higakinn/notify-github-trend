import os
import time

import jinja2

from exactractor import github
from notifier.qiita import Qiita


def main():
    program_languages = os.getenv("PROGRAM_LANGUAGES").split(",")
    article_ids = os.getenv("ARTICLE_IDS").split(",")
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
