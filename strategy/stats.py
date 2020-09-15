import numpy as np
from collections import defaultdict

class StrategyStatistics(object):
	def __init__(self):
		self.start_date = ''
		self.num_bets = 0
		self.is_out_of_money = False
		self.total_won = 0
		self.total_spent = 0
		self.profit = 0
		self.profit_per_bet = 0
		self.spent_sums = []
		self.balances = []
		self.odds_bet_on = []
		self.results = []
		self.other = defaultdict(lambda: [])

	def mark_first_date(self, start_date: str):
		self.start_date = start_date

	def update(self, spent, won, balance, odds_bet_on, bet_num=1, **argdict):
		self.num_bets += bet_num
		self.is_out_of_money = (balance <= 10.0)

		self.spent_sums.append(spent)
		self.balances.append(balance)
		self.total_won += won
		self.total_spent += spent

		self.odds_bet_on.extend(odds_bet_on)

		for k, v in argdict.items():
			self.other[k].append(v)

	def compute_stats(self):
		self.profit = (self.total_won - self.total_spent)
		self.profit_per_bet = self.profit / (self.num_bets + 0.001)

		self.avg_odd = np.average(self.odds_bet_on)

		for idx, balance in enumerate(self.balances):
			if idx == 0:
				continue
			if balance > self.balances[idx - 1]:
				self.results.append(1)
			elif balance < self.balances[idx - 1]:
				self.results.append(-1)
			else:
				self.results.append(0)
		self.results = np.cumsum(np.array([0] + self.results) * 0.1)


	def out_of_money(self):
		return self.is_out_of_money
