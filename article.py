from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Article:
  title: str
  author: str
  link: str
  content: str
  image: str
  date: str
  # tokens: List[str] = None

  def __str__(self):
    return f'Title: {self.title}\nAuthor: {self.author}\nLink: {self.link}\nContent: {self.content}\n'
  
  def to_dict(self):
    return asdict(self)