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
		if self.amount == None:
			return "You didn't specifiy an amount {} FailFish".format(self.user)
		if self.check_int():
			Raffle.RaffleActive = True
			Thread(target=self.raffle_win).start()
			print(True)
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
		from modules.bot import bot_msg
		sleep(30)
		bot_msg("The raffle for {} {} ends in 30 seconds! Type !join to enter".format(self.amount, CURRENCY))
		sleep(30)
		if(len(Raffle.RaffleEntries) == 0):
			bot_msg("Nobody entered the raffle. Guess I'll keep the points for myself MingLee")
			return ""
		winner = choice(Raffle.RaffleEntries)
		database.db_add_points_user(winner, self.amount)
		self.raffle_clear()
		bot_msg("{} won the raffle and gets {} points! FeelsGoodMan".format(winner, self.amount))

	def raffle_clear(self):
		Raffle.RaffleActive = False
		del Raffle.RaffleEntries[:]