"""
author: arotaru

Stateless strategies for betting mean naive strategies or strategies that simply do not take in acount
other details than the betting odds of the match at hand.
"""


import sys
sys.path.insert(0,'..')

from bet_details import *
from .interface import BettingStrategy
from .config import *

from typing import *


class BetAgainstDraw_ProfitOnUnderDog(BettingStrategy):
	"""
		This strategy is loosing if a draw happens.
		You don't lose money but you can only profit if the underdog team wins.
	"""
	def __init__(self, config: BettingStrategyConfig):
		self.config = config

	def __repr__(self):
		return "BetAgainstDraw_ProfitOnUnderDog"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		amount_on_fav_team = self.config.preffered_amount * \
			bet_odds.odds_of(bet_odds.underdog_team()) / bet_odds.odds_of(bet_odds.favorite_team())

		return [
			PlacedBet(bet_odds, selection=bet_odds.favorite_team(), amount=amount_on_fav_team),
			PlacedBet(bet_odds, selection=bet_odds.underdog_team(), amount=self.config.preffered_amount),
		], (self.config.preffered_amount + amount_on_fav_team)


class BetAgainstDraw_ProfitOnFavorite(BettingStrategy):
	"""
		This strategy is loosing if a draw happens.
		You don't lose money but you can only profit if the favorite team wins.
	"""

	def __init__(self, config: BettingStrategyConfig):
		self.config = config

	def __repr__(self):
		return "BetAgainstDraw_ProfitOnFavorite"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		amount_on_under_dog_team = self.config.preffered_amount * \
			bet_odds.odds_of(bet_odds.favorite_team()) / bet_odds.odds_of(bet_odds.underdog_team())

		return [
			PlacedBet(bet_odds, selection=bet_odds.favorite_team(), amount=self.config.preffered_amount),
			PlacedBet(bet_odds, selection=bet_odds.underdog_team(), amount=amount_on_under_dog_team),
		], (self.config.preffered_amount + amount_on_under_dog_team)


class BetOnFavoriteOdd(BettingStrategy):
	def __init__(self, config: BettingStrategyConfig):
		self.config = config

	def __repr__(self):
		return "BetOnFavoriteOdd"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		return [
			PlacedBet(bet_odds, selection=bet_odds.favorite_odd(), amount=self.config.preffered_amount),
		], self.config.preffered_amount


class BetAlwaysOnHome(BettingStrategy):
	def __init__(self, config: BettingStrategyConfig):
		self.config = config

	def __repr__(self):
		return "BetAlwaysOnHome"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		return [
			PlacedBet(bet_odds, selection=BetSelection.ONE, amount=self.config.preffered_amount),
		], self.config.preffered_amount


class BetAlwaysOnDraw(BettingStrategy):
	def __init__(self, config: BettingStrategyConfig):
		self.config = config

	def __repr__(self):
		return "BetAlwaysOnDraw"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		return [
			PlacedBet(bet_odds, selection=BetSelection.X, amount=self.config.preffered_amount),
		], self.config.preffered_amount


class BetAlwaysOnAway(BettingStrategy):
	def __init__(self, config: BettingStrategyConfig):
		self.config = config

	def __repr__(self):
		return "BetAlwaysOnAway"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		return [
			PlacedBet(bet_odds, selection=BetSelection.TWO, amount=self.config.preffered_amount),
		], self.config.preffered_amount


class BetOnClearFavorite(BetOnFavoriteOdd):
	def __init__(self, config: BettingStrategyConfig, **kwargs):
		self.config = config
		self.FAVORITE_THRESHOLD = 3.0

	def __repr__(self):
		return "BetOnClearFavorite"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		favorite_team = bet_odds.favorite_team()
		underdog_team = bet_odds.underdog_team()

		if bet_odds.odds_of(favorite_team) * self.FAVORITE_THRESHOLD <= bet_odds.odds_of(underdog_team):
			return [
				PlacedBet(bet_odds, selection=favorite_team, amount=self.config.preffered_amount),
			], self.config.preffered_amount
		return [], 0

class BetAroundOdd50(BettingStrategy):
	def __init__(self, config: BettingStrategyConfig, **kwargs):
		self.config = config
		self.FAVORITE_ODD = 2.0

	def __repr__(self):
		return "BetOnClearFavorite"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		favorite_odd = bet_odds.favorite_odd()

		if self.FAVORITE_ODD * 0.9 <= bet_odds.odds_of(fav_odd) and \
			bet_odds.odds_of(fav_odd) <= self.FAVORITE_ODD * 1.1:
			return [
				PlacedBet(bet_odds, selection=fav_odd, amount=self.config.preffered_amount),
			], self.config.preffered_amount
		return [], 0

class BetAgainstDraw_ProfitOnClearFavorite(BetOnClearFavorite):
	def __init__(self, config: BettingStrategyConfig):
		super().__init__(config)

	def __repr__(self):
		return "BetAgainstDraw_ProfitOnClearFavorite"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		fav_odd = bet_odds.favorite_team()
		und_odd = bet_odds.underdog_team()

		if bet_odds.odds_of(fav_odd) * self.FAVORITE_THRESHOLD <= bet_odds.odds_of(und_odd): #, bet_odds.odds_of(BetSelection.X)):
			amount_on_other_team = self.config.clip(
				self.config.preffered_amount * \
				bet_odds.odds_of(bet_odds.underdog_team()) /\
				bet_odds.odds_of(bet_odds.favorite_team())
			)
			return [
				PlacedBet(bet_odds, selection=bet_odds.favorite_team(), amount=self.config.preffered_amount),
				PlacedBet(bet_odds, selection=bet_odds.underdog_team(), amount=amount_on_other_team),
			], (self.config.preffered_amount + amount_on_other_team)
		return [], 0


class BetAgainstDraw_ProfitOnClearUnFavorite(BetOnClearFavorite):
	def __init__(self, config: BettingStrategyConfig):
		super().__init__(config)

	def __repr__(self):
		return "BetAgainstDraw_ProfitOnClearUnFavorite"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		fav_odd = bet_odds.favorite_team()
		und_odd = bet_odds.underdog_team()

		if bet_odds.odds_of(fav_odd) * self.FAVORITE_THRESHOLD <= bet_odds.odds_of(und_odd):
			amount_on_other_team = self.config.clip(
				self.config.preffered_amount * \
				bet_odds.odds_of(bet_odds.favorite_team()) /\
				bet_odds.odds_of(bet_odds.underdog_team())
			)
			return [
				PlacedBet(bet_odds, selection=bet_odds.favorite_team(), amount=self.config.preffered_amount),
				PlacedBet(bet_odds, selection=bet_odds.underdog_team(), amount=amount_on_other_team),
			], (self.config.preffered_amount + amount_on_other_team)
		return [], 0

"""
	Thse statistics are computed on our entire database of matches and odds.
	There is some weird ass shit going on. Not completly sure how or why, but maybe
	it's not the agency trying to fake their odds. These are computed on bet365 odds.
	For each interval of odds, we have the actual chance of that odd being correct, the number
	of games with those odds, and the odds as probabilities.

	Unofortunately we don't know if the odds came from the intiial estimation of the agency,
	or contain public perception as well (odds change dynamically if people bet)
	The format:
	(low_odd, high_odd): actual_chance, num_games, [high_odd_to_prob, low_odd_to_prob]
	The problem above explained in simple terms, the first number after ':' should
	be between the last two numbers (the list)
"""
HOME_ODDS_TO_ACTUAL_PROBABILITY = {
	(20.0, 100000.0): (1.0, 5, [0.0, 0.05]),
	(10.0, 20.0): (0.07, 86, [0.05, 0.1]),
	(6.67, 10.0): (0.11, 132, [0.1, 0.15]),
	(5.0, 6.67): (0.21, 253, [0.15, 0.2]),
	(4.0, 5.0): (0.77, 385, [0.2, 0.25]),
	(3.33, 4.0): (0.76, 497, [0.25, 0.3]),
	(2.86, 3.33): (0.65, 729, [0.3, 0.35]),
	(2.5, 2.86): (0.65, 903, [0.35, 0.4]),
	(2.22, 2.5): (0.38, 1164, [0.4, 0.45]),
	(2.0, 2.22): (0.56, 1181, [0.45, 0.5]),
	(1.82, 2.0): (0.52, 944, [0.5, 0.55]),
	(1.67, 1.82): (0.55, 566, [0.55, 0.6]),
	(1.54, 1.67): (0.59, 510, [0.6, 0.65]),
	(1.43, 1.54): (0.35, 375, [0.65, 0.7]),
	(1.33, 1.43): (0.28, 232, [0.7, 0.75]),
	(1.25, 1.33): (0.79, 186, [0.75, 0.8]),
	(1.18, 1.25): (0.8, 141, [0.8, 0.85]),
	(1.11, 1.18): (0.14, 130, [0.85, 0.9]),
	(1.05, 1.11): (0.12, 48, [0.9, 0.95]),
	(1.0, 1.05): (0.88, 8, [0.95, 1.0])
}

AWAY_ODDS_TO_ACTUAL_PROBABILITY = {
	(20.0, 100000.0): (0.03, 63, [0.0, 0.05]),
	(10.0, 20.0): (0.08, 300, [0.05, 0.1]),
	(6.67, 10.0): (0.88, 531, [0.1, 0.15]),
	(5.0, 6.67): (0.15, 887, [0.15, 0.2]),
	(4.0, 5.0): (0.81, 1308, [0.2, 0.25]),
	(3.33, 4.0): (0.75, 1346, [0.25, 0.3]),
	(2.86, 3.33): (0.32, 1188, [0.3, 0.35]),
	(2.5, 2.86): (0.65, 817, [0.35, 0.4]),
	(2.22, 2.5): (0.63, 642, [0.4, 0.45]),
	(2.0, 2.22): (0.46, 436, [0.45, 0.5]),
	(1.82, 2.0): (0.52, 290, [0.5, 0.55]),
	(1.67, 1.82): (0.46, 189, [0.55, 0.6]),
	(1.54, 1.67): (0.57, 159, [0.6, 0.65]),
	(1.43, 1.54): (0.7, 90, [0.65, 0.7]),
	(1.33, 1.43): (0.76, 71, [0.7, 0.75]),
	(1.25, 1.33): (0.78, 60, [0.75, 0.8]),
	(1.18, 1.25): (0.21, 47, [0.8, 0.85]),
	(1.11, 1.18): (0.12, 25, [0.85, 0.9]),
	(1.05, 1.11): (1.0, 2, [0.9, 0.95])
}

DRAW_ODDS_TO_ACTUAL_PROBABILITY = {
	(20.0, 100000.0): (1.0, 1, [0.0, 0.05]),
	(10.0, 20.0): (0.87, 45, [0.05, 0.1]),
	(6.67, 10.0): (0.93, 188, [0.1, 0.15]),
	(5.0, 6.67): (0.87, 399, [0.15, 0.2]),
	(4.0, 5.0): (0.2, 1167, [0.2, 0.25]),
	(3.33, 4.0): (0.26, 3941, [0.25, 0.3]),
	(2.86, 3.33): (0.68, 2400, [0.3, 0.35]),
	(2.5, 2.86): (0.62, 42, [0.35, 0.4]),
	(2.22, 2.5): (0.5, 2, [0.4, 0.45]),
	(2.0, 2.22): (1.0, 1, [0.45, 0.5])
}

def odd_to_interval(odds_dct:Dict, odd:float) -> Tuple[float, float]:
	for interval in odds_dct:
		if interval[0] <= odd and odd <= interval[1]:
			return interval
	return None

class BetOnRealChanceIfOddsFake(BettingStrategy):
	def __init__(self, config: BettingStrategyConfig):
		self.config = config

		self.selection_to_odds_probs = {
			BetSelection.ONE: HOME_ODDS_TO_ACTUAL_PROBABILITY,
			BetSelection.TWO: AWAY_ODDS_TO_ACTUAL_PROBABILITY,
			BetSelection.X:   DRAW_ODDS_TO_ACTUAL_PROBABILITY,
		}

	def __repr__(self):
		return "BetOnRealChanceIfOddsFake"

	def bet(self, bet_odds:BetOdds) -> Tuple[List[PlacedBet], float]:
		favorite_choice = bet_odds.favorite_odd()
		favorite_odd = bet_odds.odds_of(favorite_choice)
		favorite_prob = 1 / (favorite_odd + 0.001)

		interval = odd_to_interval(
			self.selection_to_odds_probs[favorite_choice],
			favorite_odd
		)

		if not interval:
			return [], 0

		real_prob, games_num, prob_interval = self.selection_to_odds_probs[favorite_choice][interval]

		# if probabilties are computed on less than 40 games, disregard them
		if games_num <= 40:
			return [], 0

		# this would drastically reduec the amount of considered betting odds
		if real_prob >= 0.65 and favorite_odd >= 2.0:
			amount = self.config.preffered_amount
			return [
				PlacedBet(bet_odds, selection=favorite_choice, amount=amount),
			], amount

		return [], 0



def main():
	config = BettingStrategyOptions(
		min_amount=0.1,
		max_amount=10,
		preffered_amount=1,
		balance=100
	)

	print("clipped:  20", config.clip(20))
	print("clipped: -20", config.clip(-20))

	strategies = [
		BetAgainstDraw_ProfitOnUnderDog(config),
		BetAgainstDraw_ProfitOnFavorite(config)
	]

	for odd in toy_odds:
		print("=" * 100)
		print(odd)
		print("-" * 100)
		for strategy in strategies:
			print(strategy)
			for placed_bet in strategy.bet(odd)[0]:
				print(placed_bet)


if __name__ == "__main__":
	main()
