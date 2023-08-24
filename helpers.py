from article import Article

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