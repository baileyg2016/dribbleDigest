class Rumor:
  def __init__(self, title, author, link, description):
    self.title = title
    self.author = author
    self.link = link
    self.description = description

  def __str__(self):
    return f'Title: {self.title}\nAuthor: {self.author}\nLink: {self.link}\nDescription: {self.description}\n'