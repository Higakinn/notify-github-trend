from unittest import result
import requests
from bs4 import BeautifulSoup

def get_trends(language="python", since="daily"):
  gh_base_url = "https://github.com"
  gh_trend_url = f"{gh_base_url}/trending/{language}?since={since}"
  
  gh_trend_page = requests.get(gh_trend_url)

  # Create a BeautifulSoup object
  soup = BeautifulSoup(gh_trend_page.text, 'html.parser')

  # get the repo list
  repo_list = soup.find_all(class_="Box-row")
  results = []
  for repo in repo_list:
    r = repo.find(class_='h3 lh-condensed')
    desc = repo.find('p',class_='col-9 color-fg-muted my-1 pr-4')
    star_child_tag = repo.find('svg', class_='octicon octicon-star')
    star = star_child_tag.parent.text.strip()
    trend_repo_a_tag = r.find('a')

    title = trend_repo_a_tag.get('href')
    description = getattr(desc,'text', '').lstrip()
    gh_trend_url = f"{gh_base_url}{title}"

    results.append(
      {
        'title': title[1:],
        'url': gh_trend_url,
        'description': description,
        'star': star
      }
    )

  return results