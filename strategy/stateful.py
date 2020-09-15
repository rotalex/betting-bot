"""
author: arotaru

Stateless strategies for betting mean strategies that:
	* take in acount some simple persisting state (previous bets, lost amounts)
	* the bet details at hand
"""

import numpy as np

import sys
sys.path.insert(0,'..')

from bet_details import *
from .interface import BettingStrategy
from .config import *
from .stateless import *

from typing import *

BETS_IN_THE_RED = 5

class StrategyState(object):
	def __init__(self, config: BettingStrategyConfig, **kwargs):
		self.capacity = 20
		self.history = []
		self.balances = []
		self.steps_on_red = 0
		self.steps_on_green = 0
		self.max_balance = 0


	def update(self, placed_bet:PlacedBet, balance:float):
		self.history.append(placed_bet)
		#self.history = self.history
		#self.balances.append(balance)
		self.max_balance = max(self.max_balance, balance)

		#print("\nupdate: ", self.balances[-5:], balance)
		if self.balances and self.balances[-1] <= balance:
			self.steps_on_red = 0
			self.steps_on_green += 1
		else:
			self.steps_on_red += 1
			self.steps_on_green = 0
		self.balances.append(balance)

		#self.steps_on_red = max(self.steps_on_red, 20)

	def get_max_balance(self):
		return self.max_balance


class MartingaleStrategy(BetOnRealChanceIfOddsFake, StrategyState):
	def __init__(self, config: BettingStrategyConfig, tag:str = ""):
		super().__init__(config)
		StrategyState.__init__(self, config) #needed for some reason
		self.tag = tag
		self.amount = self.config.preffered_amount
		self.sum_to_recover = 0
		#self.sum_to_recover_exponitially_decreased = 0

	def __repr__(self):
		return "MartingaleStrategy" + self.tag

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		super_placed_bets = super().bet(bet_odds)[0]
		if not super_placed_bets:
			return [], 0
		selection = super_placed_bets[0].selection # parent class choice

		if self.get_max_balance() > self.config.balance:
			#print("steps red: ", self.steps_on_red)
			sum_to_recover = self.get_max_balance() - self.config.balance + self.config.preffered_amount
			self.sum_to_recover = sum_to_recover
			amount = sum_to_recover / bet_odds.odds_of(selection)
		else:
			amount = self.config.preffered_profit / (bet_odds.odds_of(selection) - 1)

		#amount = self.config.clip(amount)

		placed_bets = [
			PlacedBet(
				bet_odds,
				selection=selection,
				amount=amount
			),
		], amount

		self.update(placed_bets, self.config.balance)
		return placed_bets

class MartingaleStrategyExponentialDecay(BetOnRealChanceIfOddsFake, StrategyState):
	def __init__(self, config: BettingStrategyConfig, decay:float=0.75, tag:str = ""):
		super().__init__(config)
		StrategyState.__init__(self, config) #needed for some reason
		self.decay = decay
		self.tag = tag
		self.amount = self.config.preffered_amount
		self.sum_to_recover = 0
		self.sum_to_recover_exponitially_decreased = 0

	def __repr__(self):
		return "MartingaleStrategy" + self.tag

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		super_placed_bets = super().bet(bet_odds)[0]
		if not super_placed_bets:
			return [], 0
		selection = super_placed_bets[0].selection # parent class choice

		if self.get_max_balance() > self.config.balance:
			#print("steps red: ", self.steps_on_red)
			sum_to_recover = self.get_max_balance() - self.config.balance + self.config.preffered_amount
			self.sum_to_recover = sum_to_recover
			sum_to_recover *= self.decay ** (self.steps_on_red + 1)
			self.sum_to_recover_exponitially_decreased = sum_to_recover
			amount = sum_to_recover / bet_odds.odds_of(selection)
		else:
			amount = self.config.preffered_profit / (bet_odds.odds_of(selection) - 1)

		#amount = self.config.clip(amount)

		placed_bets = [
			PlacedBet(
				bet_odds,
				selection=selection,
				amount=amount
			),
		], amount

		self.update(placed_bets, self.config.balance)
		return placed_bets
