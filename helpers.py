from article import Article
import json
from datetime import datetime

def dict_to_article(data, scrap_func):
  title = data['headline'].strip('!@#$%^&*()[]{};:,./<>?\|`~-=_+')
  author = data['byline'] if 'byline' in data else ''
  link = data['links']['web']['href']
  
  try:
    content = scrap_func(link)
  except Exception as e:
    # print(data)
    # print()
    content = ''
  image = data['images'][0]['url'] if data['images'] else ''
  date = data['published']
  return Article(title, author, link, content, image, date)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)
    

def get_team_logo_url(team_name: str) -> str:
  team_logos_map = {
    "Detroit Lions": 'https://static.sprtactn.co/teamlogos/nfl/100/det.png',
    "Carolina Panthers": 'https://static.sprtactn.co/teamlogos/nfl/100/car.png',
    "New England Patriots": 'https://static.sprtactn.co/teamlogos/nfl/100/ne.png',
    "Tennessee Titans": 'https://static.sprtactn.co/teamlogos/nfl/100/ten.png',
    "San Diego Chargers": 'https://static.sprtactn.co/teamlogos/nfl/100/sd.png',  # Note: Now Los Angeles Chargers
    "San Francisco 49ers": 'https://static.sprtactn.co/teamlogos/nfl/100/sf.png',
    "Buffalo Bills": 'https://static.sprtactn.co/teamlogos/nfl/100/buf.png',
    "Chicago Bears": 'https://assets.actionnetwork.com/598430_bears1.png',
    "Seattle Seahawks": 'https://static.sprtactn.co/teamlogos/nfl/100/sea.png',
    "Green Bay Packers": 'https://static.sprtactn.co/teamlogos/nfl/100/gb.png',
    "Cleveland Browns": 'https://static.sprtactn.co/teamlogos/nfl/100/cle.png',
    "Kansas City Chiefs": 'https://static.sprtactn.co/teamlogos/nfl/100/kc.png',
    "Arizona Cardinals": 'https://static.sprtactn.co/teamlogos/nfl/100/ari.png',
    "Minnesota Vikings": 'https://static.sprtactn.co/teamlogos/nfl/100/min.png',
    "New York Jets": 'https://static.sprtactn.co/teamlogos/nfl/100/nyj.png',
    "New York Giants": 'https://static.sprtactn.co/teamlogos/nfl/100/nygd.png',
    "Cincinnati Bengals": 'https://static.sprtactn.co/teamlogos/nfl/100/cin.png',
    "Atlanta Falcons": 'https://static.sprtactn.co/teamlogos/nfl/100/atl.png',
    "Baltimore Ravens": 'https://static.sprtactn.co/teamlogos/nfl/100/bal.png',
    "Dallas Cowboys": 'https://static.sprtactn.co/teamlogos/nfl/100/dal.png',
    "Denver Broncos": 'https://static.sprtactn.co/teamlogos/nfl/100/den.png',
    "Houston Texans": 'https://static.sprtactn.co/teamlogos/nfl/100/hou.png',
    "Indianapolis Colts": 'https://static.sprtactn.co/teamlogos/nfl/100/ind.png',
    "Jacksonville Jaguars": 'https://static.sprtactn.co/teamlogos/nfl/100/jax.png',
    "Las Vegas Raiders": 'https://static.sprtactn.co/teamlogos/nfl/100/lv.png',
    "Los Angeles Rams": 'https://static.sprtactn.co/teamlogos/nfl/100/lar.png',
    "Miami Dolphins": 'https://static.sprtactn.co/teamlogos/nfl/100/mia.png',
    "New Orleans Saints": 'https://static.sprtactn.co/teamlogos/nfl/100/no.png',
    "Philadelphia Eagles": 'https://static.sprtactn.co/teamlogos/nfl/100/phi.png',
    "Pittsburgh Steelers": 'https://static.sprtactn.co/teamlogos/nfl/100/pit.png',
    "Tampa Bay Buccaneers": 'https://static.sprtactn.co/teamlogos/nfl/100/tb.png',
    "Washington Football Team": 'https://static.sprtactn.co/teamlogos/nfl/100/was.png',
    "Colorado Rockies": 'https://static.sprtactn.co/teamlogos/mlb/100/col.png',
    "Tampa Bay Rays": 'https://static.sprtactn.co/teamlogos/mlb/100/tb.png',
    "Cincinnati Reds": 'https://static.sprtactn.co/teamlogos/mlb/100/cin.png',
    "Arizona Diamondbacks": 'https://static.sprtactn.co/teamlogos/mlb/100/ari.png',
    "Los Angeles Dodgers": 'https://static.sprtactn.co/teamlogos/mlb/100/ladd.png',
    "Cleveland Guardians": 'https://assets.actionnetwork.com/253329_Guardians2.png',
    "Washington Nationals": 'https://static.sprtactn.co/teamlogos/mlb/100/wsh.png',
    "New York Yankees": 'https://static.sprtactn.co/teamlogos/mlb/100/nyyd.png',
    "Boston Red Sox": 'https://static.sprtactn.co/teamlogos/mlb/100/bos.png',
    "Houston Astros": 'https://static.sprtactn.co/teamlogos/mlb/100/hou.png',
    "Toronto Blue Jays": 'https://static.sprtactn.co/teamlogos/mlb/100/tor.png',
    "Baltimore Orioles": 'https://static.sprtactn.co/teamlogos/mlb/100/bal.png',
    "Atlanta Braves": 'https://static.sprtactn.co/teamlogos/mlb/100/atl.png',
    "Chicago White Sox": 'https://static.sprtactn.co/teamlogos/mlb/100/chw.png',
    "Chicago Cubs": 'https://static.sprtactn.co/teamlogos/mlb/100/chc.png',
    "Detroit Tigers": 'https://static.sprtactn.co/teamlogos/mlb/100/det.png',
    "Kansas City Royals": 'https://static.sprtactn.co/teamlogos/mlb/100/kc.png',
    "Los Angeles Angels": 'https://static.sprtactn.co/teamlogos/mlb/100/laa.png',
    "Miami Marlins": 'https://static.sprtactn.co/teamlogos/mlb/100/mia.png',
    "Milwaukee Brewers": 'https://static.sprtactn.co/teamlogos/mlb/100/mil.png',
    "Minnesota Twins": 'https://static.sprtactn.co/teamlogos/mlb/100/min.png',
    "New York Mets": 'https://static.sprtactn.co/teamlogos/mlb/100/nym.png',
    "Oakland Athletics": 'https://static.sprtactn.co/teamlogos/mlb/100/oak.png',
    "Philadelphia Phillies": 'https://static.sprtactn.co/teamlogos/mlb/100/phi.png',
    "Pittsburgh Pirates": 'https://static.sprtactn.co/teamlogos/mlb/100/pit.png',
    "San Diego Padres": 'https://static.sprtactn.co/teamlogos/mlb/100/sd.png',
    "San Francisco Giants": 'https://static.sprtactn.co/teamlogos/mlb/100/sf.png',
    "Seattle Mariners": 'https://static.sprtactn.co/teamlogos/mlb/100/sea.png',
    "St. Louis Cardinals": 'https://static.sprtactn.co/teamlogos/mlb/100/stl.png',
    "Texas Rangers": 'https://static.sprtactn.co/teamlogos/mlb/100/tex.png'
  }
  
  for key, value in team_logos_map.items():
    if team_name in key:
      return value

  return ''



