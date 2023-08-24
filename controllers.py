from typing import List
from main import scrape_bleacher_report, get_espn_data, bleacher_report_rumor_to_article, get_betting_lines

def news_controller(favorite_sports: List[str], favorite_teams: List[str], return_as_dict: bool = False):
  articles = []
  for sport in favorite_sports:
    rumors = scrape_bleacher_report(sport)[:25]
    articles.extend([bleacher_report_rumor_to_article(rumor) for rumor in rumors])
    articles.extend(get_espn_data(sport))

  if return_as_dict:
    return [article.to_dict() for article in articles]

  return articles

def rumors_controller(favorite_sports: List[str], favorite_teams: List[str], return_as_dict: bool = False):
  rumors = []
  for sport in favorite_sports:
    rumors.extend(scrape_bleacher_report(sport))

  if return_as_dict:
    return [rumor.to_dict() for rumor in rumors]
  return rumors

def betting_lines_controller(favorite_sports: List[str], favorite_teams: List[str], return_as_dict: bool = False):
  bets = []

  for sport in favorite_sports:
    bets.extend(get_betting_lines(sport))

  if return_as_dict:
    return [bet.to_dict() for bet in bets]
  
  return bets