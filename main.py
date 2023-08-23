import requests
from bs4 import BeautifulSoup
from enum import Enum
import numpy as np
from rumor import Rumor
from article import Article
from dotenv import load_dotenv

load_dotenv()


class FavoriteSports(Enum):
  NBA = " NBA Basketball"
  NFL = "NFL Football"
  MLB = "MLB Baseball"
  SOCCER = "EPL Soccer"
  NHL = 'NHL Hockey'

SPORT_TO_NEWS_LINK = {
  FavoriteSports.NBA: 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard',
  FavoriteSports.NFL: 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/news',
  FavoriteSports.MLB: 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/news',
  FavoriteSports.NHL: 'http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news',
  FavoriteSports.SOCCER: 'http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/news',
}

def get_espn_endpoint(sport: FavoriteSports):
  id = ''
  if sport == FavoriteSports.NBA:
    id = 'basketball/nba'
  elif sport == FavoriteSports.NFL:
    id = 'football/nfl'
  elif sport == FavoriteSports.MLB:
    id = 'baseball/mlb'
  elif sport == FavoriteSports.NHL:
    id = 'hockey/nhl'
  elif sport == FavoriteSports.SOCCER:
    id = 'soccer/eng.1'

  return f'http://site.api.espn.com/apis/site/v2/sports/basketball/{id}/scoreboard'

def get_espn_data(sport: FavoriteSports):
  espn_endpoint = get_espn_endpoint(sport)
  response = requests.get(espn_endpoint)
  data = response.json()
  articles = np.array(data['articles'])
  descriptions = [article['description'] for article in articles]
  print(descriptions)
  print(len(descriptions))
  return articles

# used to get the bleacher report for rumors
# nba: https://bleacherreport.com/nba-rumors?from=sub
# nfl: https://bleacherreport.com/nfl-rumors?from=main
# nhl: https://bleacherreport.com/nhl-rumors?from=main
# mlb: https://bleacherreport.com/mlb-rumors?from=main
def scrape_bleacher_report(sport, css_class):
  url = f'https://bleacherreport.com/{sport}-rumors?from=sub'
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  rumors = []
  for news in soup.find_all('div', {'class': css_class}):  # Replace with actual class name
    title = news.find('a', {'class': 'articleTitle'}).text  # Replace with actual tag name
    author = news.find('span', {'class': 'authorInfo'}).text
    link = news.find('a', {'class': 'articleTitle'})['href']
    description = soup.find('p', {'class': 'articleDescription'}).text

    r = Rumor(title, author, link, description)
    # print(r, '\n')
    rumors.append(r)
  return rumors

# sample url: https://bleacherreport.com/articles/10087072-report-cal-stanford-smu-additions-again-under-serious-consideration-by-acc
def get_bleacher_report_article(article_url):
  response = requests.get(article_url)
  soup = BeautifulSoup(response.text, 'html.parser')

  # find the image of the article
  image_div = soup.find('div', {'class': 'articleLeadImage'})
  image_src = image_div.find('img')['src']

  # find of all of article text
  content_stream_div = soup.find('div', class_='contentStream')
  article_text = ''.join([p.get_text() for p in content_stream_div.find_all('p')])

  # find the author
  author = soup.find('span', {'class': 'name' }).text

  # find the title
  title = soup.find('article').find('header').find('h1').text
  
  # find date
  date = soup.find('span', {'class': 'date' }).text

  print(Article(title, author, article_url, article_text, image_src, date))

# get_espn_data("http://site.api.espn.com/apis/site/v2/sports/basketball/nba/news")
# scrape_bleacher_report('nba', 'articleContent')
get_bleacher_report_article('https://bleacherreport.com/articles/10087072-report-cal-stanford-smu-additions-again-under-serious-consideration-by-acc')