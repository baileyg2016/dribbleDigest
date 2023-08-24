from typing import List
from article import Article
from rumor import Rumor
import requests
import json
import re
import numpy as np

from controllers import rumors_controller, news_controller

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
  articles = news_controller(favorite_sports, favorite_teams, True)

  inputs = {
    "favorite_sports": json.dumps(favorite_sports),
    "favorite_teams": json.dumps(favorite_teams),
    "articles": json.dumps(articles[0:10]) # right now only worry about the top ten
  }
  # print(articles)
  print('--- making respell articles request ---')
  respell_resp = respell_request(
    inputs,
    spellId="1Lkc-tCYn5KSd97eGrlhZ",
    spellVersionId="lkL0hGfE7IZARcWxPorlg"
  )
  print(respell_resp)
  print(respell_resp['outputs']['output'])
  array = np.array(extract_xml_data(respell_resp['outputs']['output']).split(','))
  print(array[0])
  
def find_best_rumors(rumors_list: List[Rumor] = []):
  favorite_sports = ['nba', 'nfl']
  favorite_teams = ['Warriors', '49ers']
  rumors = rumors_controller(favorite_sports, favorite_teams, True)
  inputs = {
    "favorite_sports": favorite_sports,
    "favorite_teams": favorite_teams,
    "rumors": rumors
  }
  # print(articles)
  respell_resp = respell_request(
    inputs,
    spellId="1Lkc-tCYn5KSd97eGrlhZ",
    spellVersionId="k7fucmn0nlHAlvdeYnAbs"
  )


find_best_articles()