import requests
import re

from bs4 import BeautifulSoup

from lib.translater import translate


def _get_twitter_url(title: str):
    gh_base_url = "https://github.com"
    splited = title.split("/")
    author = splited[1]

    author_git_url = f"{gh_base_url}/{author}"
    author_git_page = requests.get(author_git_url)

    soup = BeautifulSoup(author_git_page.text, "html.parser")
    a_tags = soup.find(
        "a",
        attrs={"href": re.compile(r"https://twitter.com/.+")},
    )
    if a_tags is None:
        return None

    return a_tags.get("href", None)


def get_trends(language="python", since="daily"):
    gh_base_url = "https://github.com"
    gh_trend_url = f"{gh_base_url}/trending/{language}?since={since}"

    gh_trend_page = requests.get(gh_trend_url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(gh_trend_page.text, "html.parser")

    # get the repo list
    repo_list = soup.find_all(class_="Box-row")
    results = []
    for repo in repo_list:
        r = repo.find(class_="h3 lh-condensed")
        desc = repo.find("p", class_="col-9 color-fg-muted my-1 pr-4")
        star_child_tag = repo.find("svg", class_="octicon octicon-star")
        star = star_child_tag.parent.text.strip()
        trend_repo_a_tag = r.find("a")

        title = trend_repo_a_tag.get("href")
        description = getattr(desc, "text", "").lstrip()
        translated_res = translate(description)

        if translated_res["code"] == 200:
            description += f"\n{translated_res['text']}"

        gh_trend_url = f"{gh_base_url}{title}"

        gh_twitter_url = _get_twitter_url(title=title)
        results.append(
            {
                "title": title[1:],
                "url": gh_trend_url,
                "description": description,
                "star": star,
                "twitter_url": gh_twitter_url,
            }
        )

    return results


def fetch_trends():
    gh_base_url = "https://github.com"
    gh_trend_url = f"{gh_base_url}/trending"

    gh_trend_page = requests.get(gh_trend_url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(gh_trend_page.text, "html.parser")

    # get the repo list
    repo_list = soup.find_all(class_="Box-row")
    results = []
    for repo in repo_list:
        r = repo.find(class_="h3 lh-condensed")
        desc = repo.find("p", class_="col-9 color-fg-muted my-1 pr-4")
        star_child_tag = repo.find("svg", class_="octicon octicon-star")
        star = star_child_tag.parent.text.strip()
        trend_repo_a_tag = r.find("a")

        language_tag = repo.find("span", attrs={"itemprop": "programmingLanguage"})
        language = "None"
        if language_tag is not None:
            language = language_tag.text

        title = trend_repo_a_tag.get("href")
        description = getattr(desc, "text", "None").lstrip()
        translated_res = translate(description)

        description_ja = "None"
        if translated_res["code"] == 200:
            description_ja = translated_res["text"]

        gh_trend_url = f"{gh_base_url}{title}"
        gh_twitter_url = _get_twitter_url(title=title)

        results.append(
            {
                "title": title[1:],
                "url": gh_trend_url,
                "language": language,
                "description": description,
                "description_ja": description_ja,
                "star": star,
                "twitter_url": gh_twitter_url,
            }
        )

    return results
