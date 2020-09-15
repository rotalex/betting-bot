from collections import defaultdict
from enum import Enum
from typing import List, Dict, Optional


def prob_2_odd(prob):
	assert prob > 0 and prob <= 1
	return 1.0 / prob


class BetSelection:
	ONE = "1"   # TEAM1 WINS
	TWO = "2"   # TEAM2 WINS
	X = "X"		# DRAW
	ONEX = "1X" # TEAM1 WINS OR DRAW
	XTWO = "X2" # TEAM2 WINS OR DRAW


SELECTION_2_FT_RESULT = {
	'1': 'H',
	'2': 'A',
	'X': 'D'
}


def bet_selection_to_ft_result(selection: str) -> List[str]:
	return [SELECTION_2_FT_RESULT[symbol] for symbol in selection]


class BetOdds(object):
	"""
		Abstraction over what options we can bet on. It only offers the very trivial ones
		like rates for home team win, away, combined win & draw, etc.

	"""
	def __init__(
		self,
		id: int,
		teams: List[str],
		odds: Dict[str, float],
		competition: Optional[str],
		eliminatory: Optional[int], # 0=no eliminatory, 1=eliminatory in 1 round, 2=eliminatory in 2 rounds
		date: Optional[str] = ""
	):
		if len(teams) != 2:
			raise ValueError(f"There should be 2 teams in a bet odds but given: {teams}")

		if len(odds) < 3:
			raise ValueError(f"There should be 3 odds in a bet odds but given: {odds}")

		if min(odds.values()) < 1.0:
			raise ValueError(f"Odds value are invalid: {odds}. Values needs to be greater than 1.")

		self.id = id
		self.teams = teams
		self.odds = defaultdict(lambda: 1.0)
		self.odds.update(odds)
		self.competition = competition
		self.eliminatory_scheme = eliminatory
		self.date = date

	def eliminatory(self) -> bool:
		return (self.eliminatory_scheme == 1)

	def same_odds_for_win(self) -> bool:
		return self.odds[BetSelection.ONE] == self.odds[BetSelection.TWO]

	def favorite_odd(self) -> str:
		favorite_team = self.favorite_team()
		if self.odds_of(favorite_team) > self.odds_of(BetSelection.X):
			return BetSelection.X
		return favorite_team

	def favorite_team(self) -> str:
		return BetSelection.ONE \
			if self.odds[BetSelection.ONE] < self.odds[BetSelection.TWO] \
			else BetSelection.TWO

	def underdog_team(self) -> str:
		return BetSelection.ONE \
			if self.odds[BetSelection.TWO] < self.odds[BetSelection.ONE] \
			else BetSelection.TWO

	def odds_of(self, selection: str) -> float:
		return self.odds[selection] if selection in self.odds else 0

	def __str__(self) -> str:
		t1_repr = self.teams[0][:5]
		t2_repr = self.teams[1][:5]

		win1_odd = "%0.2f" % self.odds[BetSelection.ONE]
		win1_draw_odd = "%0.2f" % self.odds[BetSelection.ONEX]
		draw_odd = "%0.2f" % self.odds[BetSelection.X]
		win2_draw_odd = "%0.2f" % self.odds[BetSelection.XTWO]
		win2_odd = "%0.2f" % self.odds[BetSelection.TWO]

		return f"[{t1_repr}]" + \
				f" {win1_odd} |1x {win1_draw_odd}|" + \
				f"x {draw_odd}|" + \
				f"x2 {win2_draw_odd}|{win2_odd}" + \
				f" [{t2_repr}] " + self.competition[:8]


class PlacedBet(object):
	def __init__(
		self,
		bet_odds: BetOdds,
		selection: BetSelection,
		amount: float
	):
		self.bet_odds = bet_odds
		self.selection = selection
		self.amount = amount

	def __repr__(self):
		return str(self.bet_odds) + " Selected: " + \
			self.selection + " " + str(self.amount) +"$"


toy_odds = [
	BetOdds(
		id = 0,
		teams = ["Sevilla", "Inter"],
		odds = {
			BetSelection.ONE: 3.45,
			BetSelection.TWO: 2.1,
			BetSelection.X: 3.5,
			BetSelection.ONEX: prob_2_odd(2/3),
			BetSelection.XTWO: prob_2_odd(1/3),
		},
		competition = "CL",
		eliminatory = 1
	),
	BetOdds(
		id = 0,
		teams = ["Lyon", "Bayern Munich"],
		odds = {
			BetSelection.ONE: prob_2_odd(0.08),
			BetSelection.TWO: prob_2_odd(0.8),
			BetSelection.X:   prob_2_odd(0.12),
			BetSelection.ONEX: prob_2_odd(0.14),
			BetSelection.XTWO: prob_2_odd(0.86),
		},
		competition = "CL",
		eliminatory = 1
	),
	BetOdds(
		id = 0,
		teams = ["PSG", "Bayern Munich"],
		odds = {
			BetSelection.ONE: 3.3,
			BetSelection.TWO: 2.05,
			BetSelection.X:   4.0,
			BetSelection.ONEX: prob_2_odd(0.14),
			BetSelection.XTWO: prob_2_odd(0.86),
		},
		competition = "CL",
		eliminatory = 1
	),
]


def main():
	for odd in toy_odds:
		print(odd)


if __name__ == "__main__":
	main()
