import logging, coloredlogs
from threading import Thread
from random import choice
from time import sleep

from modules.config import *
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Raffle:

	RaffleActive = False
	RaffleEntries = []

	def __init__(self, user, amount, time):
		self.user = user
		self.amount = amount
		self.time = time

	def start_raffle(self):
		print("Amount:", self.amount)

		if self.amount == None:
			return "You didn't specifiy an amount {} FailFish".format(self.user)

		if self.check_int():
			Raffle.RaffleActive = True
			# Thread(target=self.raffle_win).start()

			return "A raffle has started for {} points! Type !join to enter PogChamp".format(self.amount)	
		else:
			return "You can only enter int values {} FailFish".format(self.user)

	def check_int(self):
		try:
			val = int(self.amount)
			return True
		except ValueError:
			return False

	def raffle_win(Thread):
		sleep(10)
		return "test123"
		winner = choice(Raffle.RaffleEntries)
		database.db_add_points_user(winner, self.amount)
		print("{} won the raffle and gets {} points! FeelsGoodMan".format(self.user, self.amount))
		return "{} won the raffle and gets {} points! FeelsGoodMan".format(self.user, self.amount)