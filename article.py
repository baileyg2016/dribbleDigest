class Article:
  def __init__(self, title, author, link, content, image, date):
    self.title = title
    self.author = author
    self.link = link
    self.content = content
    self.image = image
    self.date = date

  def __str__(self):
    return f'Title: {self.title}\nAuthor: {self.author}\nLink: {self.link}\Content: {self.content}\n'