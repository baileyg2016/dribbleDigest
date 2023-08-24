from dataclasses import dataclass

@dataclass
class Article:
  title: str
  author: str
  link: str
  content: str
  image: str
  date: str

  def __str__(self):
    return f'Title: {self.title}\nAuthor: {self.author}\nLink: {self.link}\nContent: {self.content}\n'