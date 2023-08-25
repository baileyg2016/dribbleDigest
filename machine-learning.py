from typing import List
from article import Article
from rumor import Rumor
import requests
import json
import re
import numpy as np
import xml.etree.ElementTree as ET
from bets import Bet
from helpers import DateTimeEncoder

from controllers import rumors_controller, news_controller, betting_lines_controller

#### XML PARSING ####
def extract_array_from_xml(xml_string: str):
  root = ET.fromstring(xml_string)
  articles = root.text
  # Convert the string to a list of integers
  articles_list = json.loads(articles)
  return np.array(articles_list)

def extract_xml_data(xml: str):
  match = re.search('<articles>(.*?)</articles>', xml)
  if match:
    content = match.group(1)


  return content

def extract_array_from_string(string: str):
  match = re.search('\[.*\]', string)
  if match:
      json_str = match.group(0)
      articles = json.loads(json_str.replace("'", "\""))
      # print(articles)


def respell_request(inputs, spellId: str, spellVersionId: str):
  # print(inputs)
  resp = requests.post(
    "https://api.respell.ai/v1/run",
    headers={
      # This is your API key
      "Authorization": "Bearer c0ba2a52-5395-492e-a656-5873ab45648f",
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    data=json.dumps({
      "spellId": spellId,
      # This field can be omitted to run the latest published version
      "spellVersionId": spellVersionId,
      # Fill in values for each of your 3 dynamic input blocks
      "inputs": inputs
    }),
  )

  return resp.json()

def find_best_articles(articles_list: List[Article] = []):
  favorite_sports = ['nba', 'nfl']
  favorite_teams = ['Warriors', '49ers']
  articles = np.array(news_controller(favorite_sports, favorite_teams, True))

  inputs = {
    "favorite_sports": json.dumps(favorite_sports),
    "favorite_teams": json.dumps(favorite_teams),
    "articles": json.dumps([a['title'] for a in articles]) # right now only worry about the top ten
  }
  # print(articles)
  print('--- making respell articles request ---')
  respell_resp = respell_request(
    inputs,
    spellId="1Lkc-tCYn5KSd97eGrlhZ",
    spellVersionId="c-TTfTxVgzSSwm8x9Bo9A"
  )

  if 'outputs' not in respell_resp:
    # just assume it was an error from now
    print(f'there was an error {respell_resp["message"]}')

  best_articles_indices = extract_array_from_xml(respell_resp['outputs']['output'])
  # print(best_articles_indices)
  best_articles = articles[best_articles_indices]
  # print(best_articles)
  # print(len(best_articles))
  return best_articles
  
def find_best_rumors(rumors_list: List[Rumor] = []):
  favorite_sports = ['nba', 'nfl']
  favorite_teams = ['Warriors', '49ers']
  rumors = np.array(rumors_controller(favorite_sports, favorite_teams, True))

  inputs = {
    "favorite_sports": json.dumps(favorite_sports),
    "favorite_teams": json.dumps(favorite_teams),
    "rumors": json.dumps([a['description'] for a in rumors[0:100]])
  }

  respell_resp = respell_request(
    inputs,
    spellId="dWnB1xKf20U5A--N0TXjP",
    spellVersionId="SqJEUOujVvph9D_rHR_Ko"
  )

  best_rumors_indices = np.array(json.loads(respell_resp['outputs']['output'].strip()), dtype=int)  
  return rumors[best_rumors_indices]

def get_email_subject(article_contents: List[str]):
  inputs = {
    "articles_combined_content": json.dumps('\n'.join(article_contents))
  }

  respell_resp = respell_request(
    inputs,
    spellId="-CpwV_-l3ovtyOEmPzxA_",
    spellVersionId="9rCxjWN9R_V-fJXe-Twtz"
  )

  if 'outputs' not in respell_resp:
    # just assume it was an error from now
    print(f'there was an error {respell_resp["message"]}')
  print(respell_resp['outputs']['output'])
  return respell_resp['outputs']['output']

# we are assuming that bets is of python list type
def get_best_betting_lines(bets: List[Bet]):
  favorite_sports = ['nba', 'nfl']
  favorite_teams = ['Warriors', '49ers']
  bets = np.array(betting_lines_controller(favorite_sports, favorite_teams, True))

  inputs = {
    "favorite_sports": json.dumps(favorite_sports),
    "favorite_teams": json.dumps(favorite_teams),
    "bets": json.dumps(bets.tolist(), cls=DateTimeEncoder) 
  }

  respell_resp = respell_request(
    inputs,
    spellId="wWlc0jFJ8Ouf4zXsr0m7W",
    spellVersionId="5pjVM3-minWHDUaGifWUo"
  )
  print('model output', respell_resp['outputs']['output'])
  best_bets_indices = extract_array_from_xml(respell_resp['outputs']['output'])
  print(best_bets_indices)
  print(bets[best_bets_indices])
  return bets[best_bets_indices]

# testing articles
# find_best_articles()

# testing betting
# with open('/Users/baileyspell/Desktop/sample-bets.json', 'r') as f:
#   bets = json.load(f)['bets']
#   get_best_betting_lines(bets)

# testing subject line
# with open('/Users/baileyspell/Desktop/sample-articles.json', 'r') as f:
#   articles = json.load(f)
#   get_email_subject([a['content'] for a in articles])

# testing rumors
# find_best_rumors()