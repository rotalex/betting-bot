import sys
sys.path.insert(0, '..')

from typing import *
from bet_details import *
from .config import BettingStrategyConfig

class BettingStrategy(object):

	def state(self) -> BettingStrategyConfig:
		return self.config

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		...
