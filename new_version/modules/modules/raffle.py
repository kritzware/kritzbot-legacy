import logging, coloredlogs
from threading import Thread
from random import choice

from modules.config import *
from modules.timer import Timer
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

RaffleEntries = []

class Raffle:

	def __init__(self, user, amount):
		self.user = user
		self.amount = amount
		self.raffle_timer = Timer(self.user, 5, RaffleEntries, "RaffleTimer")

	def start_raffle(self):
		print("Amount:", self.amount)

		if self.amount == None:
			return "You didn't specifiy an amount {} FailFish".format(self.user)

		if self.check_int():
			Thread(target=self.raffle_timer.raffle_run).start()
			return "A raffle has started for {} points! Type !join to enter PogChamp".format(self.amount)
		else:
			return "You can only enter int values {} FailFish".format(self.user)

	def check_int(self):
		try:
			val = int(self.amount)
			return True
		except ValueError:
			return False

	def raffle_win(self):
		winner = choice(RaffleEntries)
		database.db_add_points_user(winner, self.amount)
		return "{} won the raffle and gets {} points! FeelsGoodMan".format(self.user, self.amount)