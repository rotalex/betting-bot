import numpy as np

from typing import *


class BettingStrategyConfig(object):
	def __init__(self, balance: float):
		self.balance = balance



class BetStrategyConfigAbsolut(BettingStrategyConfig):
	def __init__(
		self,
		min_amount: float,
		max_amount: float,
		preffered_amount: float,
		preffered_profit: float,
		balance: float,
	):
		super().__init__(balance)
		self.min_amount = min_amount
		self.max_amount = max_amount
		self.preffered_amount = preffered_amount
		self.preffered_profit = preffered_profit

	def insuficient_funds(self):
		return (self.preffered_amount > self.balance)

	def clip(self, val: float) -> float:
		return np.clip(val, self.min_amount, self.max_amount)


class BettingStrategyConfigPercent(BettingStrategyConfig):
	def __init__(
		self,
		min_amount: float,
		max_amount: float,
		preffered_amount: float,
		preffered_profit: float,
		balance: float,
	):
		super().__init__(balance)
		self.min_amount = min_amount
		self.max_amount = max_amount
		self.preffered_amount = preffered_amount
		self.preffered_profit = preffered_profit

	def insuficient_funds(self):
		return (self.preffered_amount * self.balance > self.balance)

	def clip(self, val: float) -> float:
		return np.clip(
			val,
			self.min_amount * self.balance,
			self.max_amount * self.balance,
		)
