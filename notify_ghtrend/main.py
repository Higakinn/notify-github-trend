import os

import jinja2

from exactractor import github
from notifier.qiita import Qiita


def main():
    program_languages = os.getenv("PROGRAM_LANGUAGES").split(",")
    for program_language in program_languages:
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
        Qiita().post(program_language, title, md_content)


if __name__ == "__main__":
    main()
