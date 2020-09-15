import numpy as np
import pandas as pd

from collections import defaultdict
from typing import List
from tqdm import tqdm

from betting_agency import BettingAgency, Bet365
from strategy.interface import BettingStrategy
from strategy.stats import StrategyStatistics


class Simulation(object):
	def __init__(
		self,
		agencies: List[BettingAgency],
		strategies: List[BettingStrategy]
	):
		self.agencies = agencies
		self.strategies = strategies

		self.strategy2statistics = defaultdict(lambda: StrategyStatistics())
		self.verbose = False

	def simulate(self):

		for agency in self.agencies:
			for strategy in self.strategies:
				key = (str(agency), str(strategy))
				stats = self.strategy2statistics[key]

				for bet_odds in tqdm(agency.get_betting_oddset()):

					if self.verbose:
						print("=" * 100)
						print("current balance: ", strategy.config.balance)
						print(bet_odds)

					if not stats.start_date:
						stats.mark_first_date(bet_odds.date)

					placed_bets, _ = strategy.bet(bet_odds)
					spent, won = agency.evaluate(agency.csv, placed_bets)
					strategy.config.balance += (won - spent)

					if self.verbose:
						print("PlacedBets: ", placed_bets)
						print("Evaluated: ", spent, won)
						print("Balance: ", strategy.config.balance)

					argdict = {}
					if hasattr(strategy, "sum_to_recover"):
						argdict["sum_to_recover"] = strategy.sum_to_recover
					if hasattr(strategy, "sum_to_recover_exponitially_decreased"):
						argdict["sum_to_recover_exponitially_decreased"] = \
							strategy.sum_to_recover_exponitially_decreased
					if hasattr(strategy, "steps_on_red"):
						argdict["steps_on_red"] = strategy.steps_on_red

					stats.update(
						spent, won,
						strategy.state().balance,
						odds_bet_on=[pb.bet_odds.odds[pb.selection] for pb in placed_bets],
						bet_num=len(placed_bets),
						**argdict,
					)

					if stats.out_of_money():
						break

	def stats_to_df(self) -> pd.DataFrame():
		rows = []

		for (agency_name, strategy_name), stats in self.strategy2statistics.items():
			stats.compute_stats()
			rows.append(
				{
					"agency": agency_name,
					"strategy": strategy_name,
					"start_date": stats.start_date,
					"num_bets": stats.num_bets,
					"is_out_of_money": stats.is_out_of_money,
					"total_won": stats.total_won,
					"total_spent": stats.total_spent,
					"profit": stats.profit,
					"profit_per_bet": stats.profit_per_bet,
					"avg_odd": stats.avg_odd,
					"spent_sums": np.around(np.array(stats.spent_sums), decimals=2),
					"balances": np.around(np.array(stats.balances), decimals=2),
					"results": np.around(np.array(stats.results), decimals=2),
					"sum_to_recover": np.around(np.array(stats.other['sum_to_recover']), decimals=2),
					"sum_to_recover_exponitially_decreased": \
						np.around(np.array(stats.other['sum_to_recover_exponitially_decreased']), decimals=2),
					"steps_on_red":  np.around(np.array(stats.other['steps_on_red']), decimals=2),
				}
			)

		return pd.DataFrame(rows)
