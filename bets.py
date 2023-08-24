from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Bet:
  home_team: str
  away_team: str
  game_date: datetime
  away_open: float
  home_open: float
  best_odds: float
  away_team_bets_odds: float
  home_team_bets_odds: float
  away_team_bets_percentage: float
  home_team_bets_percentage: float
  
  def __str__(self):
    return f'Home Team: {self.home_team}\nAway Team: {self.away_team}\nGame Date: {self.game_date}\nAway Open: {self.away_open}\nHome Open: {self.home_open}\nBest Odds: {self.best_odds}\nAway Team Bets Odds: {self.away_team_bets_odds}\nHome Team Bets Odds: {self.home_team_bets_odds}\nAway Team Bets Percentage: {self.away_team_bets_percentage}\nHome Team Bets Percentage: {self.home_team_bets_percentage}\n'
  
  def to_dict(self):
    return asdict(self)
