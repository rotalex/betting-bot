from bet_details import BetOdds, PlacedBet, BetSelection, bet_selection_to_ft_result
from typing import List, Tuple, Optional

import pandas as pd

class BettingAgency(object):
	"""Abstraction over the betting agency."""

	def get_betting_oddset(self, count: int = 1):
		...

	def evaluate(self, csv, placed_bets: List[PlacedBet]) -> Tuple[float, float]:
		spent = 0
		earned = 0

		for placed_bet in placed_bets:
			selected_outcomes = bet_selection_to_ft_result(placed_bet.selection)
			match = csv.iloc[placed_bet.bet_odds.id]

			if match.FullTimeResult in selected_outcomes:
				earned += placed_bet.amount * placed_bet.bet_odds.odds_of(placed_bet.selection)
			spent += placed_bet.amount

		return spent, earned


class Bet365(BettingAgency):
	def __init__(
		self,
		csv_path:str,
		num_games : float = 1.0,
		constraints : Optional[List[Tuple[str, object]]] = []
	):
		self.num_games = num_games
		self.csv = pd.read_csv(
			csv_path,
			parse_dates=['MatchDate']
		)

		for contraint in constraints:
			self.csv = self.csv[self.csv[contraint[0]] == contraint[0]]

	def __repr__(self):
		return "B365"


	def get_betting_oddset(self) -> List[BetOdds]:
		if self.num_games <= 1.0:
			limit = int(self.csv.shape[0] * self.num_games)
		else:
			limit = int(self.num_games)

		for idx, row in self.csv.iterrows():
			if idx >= limit:
				break
			try:
				odds = BetOdds(
					id = idx,
					teams = [row.HomeTeam, row.AwayTeam],
					odds = {
						BetSelection.ONE: row.Bet365homewinodds,
						BetSelection.TWO: row.Bet365drawodds,
						BetSelection.X:   row.Bet365awaywinodds,
					},
					competition = row.LeagueDivision,
					eliminatory = 0,
					date = row['MatchDate'],
				)
			except ValueError:
				continue
			yield odds

class RandomIdealAgency(BettingAgency):
	ID = 0
	def __init__(
		self,
		num_games: int = 1000000,
	):
		self.num_games = num_games
		self.id = ID
		RandomIdealAgency.ID += 1

		self.domains = {
			"divisions": ["Liga1", "L2", "L0", "L3"],
			"Teams": [f"T{id}" for id in range(0, 1000)]
		}

	def __str__(self):
		return "Random#" + str(self.id)


	def get_betting_oddset(self) -> List[BetOdds]:
		for idx in range(0, self.num_games):
			try:
				odds = BetOdds(
					id = idx,
					teams = [row.HomeTeam, row.AwayTeam],
					odds = {
						BetSelection.ONE: row.Bet365homewinodds,
						BetSelection.TWO: row.Bet365drawodds,
						BetSelection.X:   row.Bet365awaywinodds,
					},
					competition = row.LeagueDivision,
					eliminatory = 0,
					date = row['MatchDate'],
				)
			except ValueError:
				continue
			yield odds


def main():
	a = Bet365('/home/rotaru/Desktop/play/bet-agent/data/b365_big_leagues_matches.csv')
	for odds in a.get_betting_oddset():
		print(odds)

if __name__ == "__main__":
	main()
