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

# sample article: https://www.espn.com/nba/story/_/id/38241515/nbpa-filing-grievance-says-james-harden-violate-rules
def scrape_espn_article(url = 'https://www.espn.com/nba/story/_/id/38241515/nbpa-filing-grievance-says-james-harden-violate-rules'):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')

  article_tag = soup.find('div', { 'class': 'main-content'})
  title = article_tag.find('header').find('h1').text

  article_body = article_tag.find('div', { 'class': 'article-body'})
  article_text = ''.join([p.get_text() for p in article_body.find_all('p')])
  
  meta_data = article_body.find('div', { 'class': 'author'}).text.split('ESPN')
  # meta_data looks like this: ['Tim Bontemps, ', 'Aug 22, 2023, 07:27 PM ET']
  author = meta_data[0]
  date = ','.join(meta_data[1].split(",")[0:2]).strip()
  
  a = Article(title, author, url, article_text, '', date)
  print(a)

# used to get the bleacher report for rumors
# nba: https://bleacherreport.com/nba-rumors?from=sub
# nfl: https://bleacherreport.com/nfl-rumors?from=main
# nhl: https://bleacherreport.com/nhl-rumors?from=main
# mlb: https://bleacherreport.com/mlb-rumors?from=main
def scrape_bleacher_report(sport, css_class = 'articleContent'):
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
# get_bleacher_report_article('https://bleacherreport.com/articles/10087072-report-cal-stanford-smu-additions-again-under-serious-consideration-by-acc')
scrape_espn_article()