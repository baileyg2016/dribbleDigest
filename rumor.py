from dataclasses import dataclass, asdict

@dataclass
class Rumor:
  title: str
  author: str
  link: str
  description: str

  def __str__(self):
    return f'Title: {self.title}\nAuthor: {self.author}\nLink: {self.link}\nDescription: {self.description}\n'
  
  def to_dict(self):
    return asdict(self)