import requests
from bs4 import BeautifulSoup
from enum import Enum
import numpy as np
from rumor import Rumor
from article import Article
from dotenv import load_dotenv
from bets import Bet
from typing import List
from datetime import datetime
from pytz import timezone

from helpers import dict_to_article

load_dotenv()

class FavoriteSports(Enum):
  NBA = " NBA Basketball"
  NFL = "NFL Football"
  MLB = "MLB Baseball"
  SOCCER = "EPL Soccer"
  NHL = 'NHL Hockey'

class Sport(Enum):
  NFL = 'nfl'
  NBA = 'nba'
  MLB = 'mlb'
  NHL = 'nhl'

SPORT_TO_NEWS_LINK = {
  FavoriteSports.NBA: 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard',
  FavoriteSports.NFL: 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/news',
  FavoriteSports.MLB: 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/news',
  FavoriteSports.NHL: 'http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news',
  FavoriteSports.SOCCER: 'http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/news',
}

def get_espn_endpoint(sport: Sport):
  switcher = {
    Sport.NBA.value: 'basketball/nba',
    Sport.NFL.value: 'football/nfl',
    Sport.MLB.value: 'baseball/mlb',
    Sport.NHL.value: 'hockey/nhl',
    # Sport.SOCCER.value: 'soccer/eng.1',
  }

  return f'http://site.api.espn.com/apis/site/v2/sports/{switcher.get(sport)}/news'

# sample article: https://www.espn.com/nba/story/_/id/38241515/nbpa-filing-grievance-says-james-harden-violate-rules
def scrape_espn_article(url = 'https://www.espn.com/nba/story/_/id/38241515/nbpa-filing-grievance-says-james-harden-violate-rules') -> Article:
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
  
  return Article(title, author, url, article_text, '', date)

def get_espn_article_body(url) -> str:
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  article_tag = soup.find('div', { 'class': 'main-content'})
  article_body = article_tag.find('div', { 'class': 'article-body'})
  article_text = ''.join([p.get_text() for p in article_body.find_all('p')])

  return article_text

def get_espn_data(sport: FavoriteSports):
  espn_endpoint = get_espn_endpoint(sport)
  response = requests.get(espn_endpoint)
  data = response.json()
  articles = np.array(data['articles'])
  return [dict_to_article(data, get_espn_article_body) for data in articles]

# used to get the bleacher report for rumors
# nba: https://bleacherreport.com/nba-rumors?from=sub
# nfl: https://bleacherreport.com/nfl-rumors?from=main
# nhl: https://bleacherreport.com/nhl-rumors?from=main
# mlb: https://bleacherreport.com/mlb-rumors?from=main
# DONE
def scrape_bleacher_report(sport, css_class = 'articleContent') -> List[Rumor]:
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
def get_bleacher_report_article(article_url) -> Article:
  response = requests.get(article_url)
  soup = BeautifulSoup(response.text, 'html.parser')
  print(article_url)
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
  date = ''
  try:
    date = soup.find('span', {'class': 'date' }).text
  except Exception:
    pass

  return Article(title, author, article_url, article_text, image_src, date)

def scrape_the_ringer_article(article_url) -> Article:
  response = requests.get(article_url)
  soup = BeautifulSoup(response.text, 'html.parser')

  title = soup.find('h1', {'class': 'c-page-title'}).text
  author = soup.find('span', {'class': 'c-byline__author-name'}).text
  date = soup.find('time', {'class': 'c-byline__item'}).text
  image = soup.find('picture', {'class': 'c-picture'}).find('img')['src']

  body_div = soup.find('div', {'class': 'c-entry-content'})
  article_text = ''.join([p.get_text() for p in body_div.find_all('p')])
  return Article(title, author, article_url, article_text, image, date)

def bleacher_report_rumor_to_article(rumor: Rumor) -> Article:
  if (rumor.link.find('theringer') != -1):
    return scrape_the_ringer_article(rumor.link)
  if (rumor.link.find('bleacherreport') != -1):
    return get_bleacher_report_article(rumor.link)
  
  return Article(rumor.title, rumor.author, rumor.link, '', '', '')

def get_betting_lines(sport: str) -> List[Bet]:
  url = f'https://www.actionnetwork.com/{sport}/public-betting'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')

  # find the table
  public_betting_table = soup.find('div', {'class': 'public-betting__table-container'})
  rows = public_betting_table.find_all('tr')[1:]
  bets = []
  for r in rows:
    if len(r.find_all('div', class_='game-info__team--desktop')) == 0:
      continue
    # Extract time from div
    game_date = None
    link = r.find('a')
    if link and link.get('href'):
      href = r.find('a')['href']
      date_str = href.split('/')[-2]
      time_str = r.find('div', class_='public-betting__game-status').text.strip()
      date_str = ' '.join(date_str.split('odds-')[1].split('-'))
      date_time_str = f'{date_str} {time_str}'
      if date_time_str.find('Final') != -1:
        game_date = 'Final'
      elif date_time_str.find('Postponed') != -1 or date_time_str.find('TOP') != -1 or date_time_str.find('BOT') != -1:
        game_date = 'Playing'
      else:
        try:
          # Combine date and time into a single datetime object
          date = datetime.strptime(date_time_str, "%B %d %Y %I:%M %p")
          date = date.replace(tzinfo=timezone('UTC'))
          game_date = date.astimezone(timezone('US/Pacific'))
        except Exception:
          game_date = ''

    away_team = r.find_all('div', class_='game-info__team--desktop')[0].span.text
    home_team = r.find_all('div', class_='game-info__team--desktop')[1].span.text

    away_open = r.find_all('div', class_='public-betting__open-cell')[0].text
    home_open = r.find_all('div', class_='public-betting__open-cell')[1].text
    best_odds = 0.0# float(r.find('span', class_='css-1qynun2 ena22472').text)

    away_team_bet_odds = r.find_all('div', class_='book-cell__odds')[0].span.text.strip('%')
    home_team_bet_odds = r.find_all('div', class_='book-cell__odds')[1].span.text.strip('%')

    away_team_bets_percentage = None
    home_team_bets_percentage = None
    if len(r.find_all('span', class_='highlight-text__children')) > 0:
      away_team_bets_percentage = r.find_all('span', class_='highlight-text__children')[0].text
      home_team_bets_percentage = r.find_all('span', class_='highlight-text__children')[1].text

    b = Bet(home_team, away_team, game_date, away_open, home_open, best_odds, away_team_bet_odds, home_team_bet_odds, away_team_bets_percentage, home_team_bets_percentage)
    bets.append(b)
  
  return bets



# get_espn_data("http://site.api.espn.com/apis/site/v2/sports/basketball/nba/news")
# scrape_bleacher_report('nba', 'articleContent')
# get_bleacher_report_article('https://bleacherreport.com/articles/10087072-report-cal-stanford-smu-additions-again-under-serious-consideration-by-acc')
# scrape_espn_article()

# get_betting_lines(Sport.NFL)
# the ringer
# action network