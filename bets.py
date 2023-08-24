from dataclasses import dataclass
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
  
