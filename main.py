import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

from copy import deepcopy

from betting_agency import Bet365
from simulation import Simulation

from strategy.config import *
from strategy.stateless import *
from strategy.stateful import *


def main():

	cfg_abs = BetStrategyConfigAbsolut(
		min_amount=0.001,
		max_amount=10.00,
		preffered_amount=0.000001,
		preffered_profit=0.1,
		balance=100,
	)

	cfg_rel = BettingStrategyConfigPercent(
		min_amount=0.0001,
		max_amount=0.05,
		preffered_amount=1.0,
		preffered_profit=1.0,
		balance=1000,
	)

	simulator = Simulation(
		agencies = [
			Bet365('/home/rotaru/Desktop/play/bet-agent/data/b365_big_leagues_matches.csv') #, num_games=4000),
		],
		strategies = [
			MartingaleStrategy(BetStrategyConfigAbsolut(
				min_amount=0.000000000001,
				max_amount=10.00,
				preffered_amount=a,
				preffered_profit=0.1,
				balance=100,
			), tag=str(a)) \
 			for a in [\
				#1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001, 0.00005, 0.00001, 0.000005, 0.000001
				0.0001, #0.00005, 0.00001, 0.000005, 0.000001
			]
			#BetOnClearFavorite(deepcopy(cfg_abs)),
			#BetOnRealChanceIfOddsFake(deepcopy(cfg_abs)),
		]
	)

	simulator.simulate()
	stats = simulator.stats_to_df()

	print(
		stats.drop(
			columns=[
				'spent_sums', 'balances', 'results', 'sum_to_recover', #'sum_to_recover_exponitially_decreased',
				'steps_on_red'
			]
		).sort_values(
			by=['profit', 'profit_per_bet']
		)
	)
	stats.to_csv('results/strategy_comparison.csv')

	df_dct = {}
	mx_len = -1
	for idx, strategy_stats in stats.iterrows():
		df_dct[strategy_stats.strategy] = strategy_stats.balances
		mx_len = max(mx_len, len(strategy_stats.balances))

	for k, v in df_dct.items():
		print(k, len(v))
		if len(v) <= mx_len:
			df_dct[k] = np.array(list(v) + [0] * (mx_len - len(v))) # [:1500]

	for k, v in df_dct.items():
		print(k, len(v))

	df = pd.DataFrame(df_dct)
	sns.lineplot(
		data=df,
		#markers=('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
	)

	for i in range(stats.shape[0]):
		#break
		#sns.lineplot(
		#	x=range(len(stats.iloc[i].spent_sums)),
		#	y=stats.iloc[i].spent_sums
		#)

		#sns.lineplot(
		#	x=range(len(stats.iloc[i].results)),
		#	y=stats.iloc[i].results
		#)

		sns.lineplot(
			x=range(len(stats.iloc[i].sum_to_recover)),
			y=stats.iloc[i].sum_to_recover, color='orange',
			legend='brief', label="sum to recover"
		)

		#sns.lineplot(
		#	x=range(len(stats.iloc[i].sum_to_recover_exponitially_decreased)),
		#	y=stats.iloc[i].sum_to_recover_exponitially_decreased
		#)

		sns.lineplot(
			x=range(len(stats.iloc[i].steps_on_red)),
			y=-stats.iloc[i].steps_on_red,
			color='red', legend='brief', label="steps of continous loss"

		)
	plt.show()

if __name__ == "__main__":
	main()
