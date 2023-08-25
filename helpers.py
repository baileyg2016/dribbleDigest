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