import logging, coloredlogs
from random import choice, randrange
from threading import Thread

from modules.config import *
from modules.timer import Timer
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

RouletteCooldown = []

class Points:

	DuelUsers = []
	DuelOpponents = []

	def __init__(self, user):
		self.user = user
		self.currency = CURRENCY
		self.cooldown_timer = Timer(self.user, 120, RouletteCooldown, "Roulette")

	def roulette(self, amount):
		from modules.bot import bot_msg, bot_msg_whsp
		if(self.user in self.cooldown_timer.timer_list):
			return ""
		else:
			get_user_points = database.db_get_user_points_int(self.user)
			if(int(amount) > get_user_points):
				bot_msg_whsp("You don't have {} {} {} FailFish".format(amount, CURRENCY, self.user), self.user)
				return ""
			if(int(amount) <= 0):
				return ""
			gamble = randrange(1, 4)
			if(gamble == 1):
				total_win = int(amount) * 2
				database.db_add_points_user(self.user, total_win)
				output = "{} won {} {}! PogChamp".format(self.user, total_win, self.currency)
			else:
				database.db_minus_points_user(self.user, amount)
				output = "{} lost {} {}! BibleThump".format(self.user, amount, self.currency)
			Thread(target=self.cooldown_timer.cooldown_run).start()
			return output

	def givepoints(self, reciever, amount):
		if self.user == reciever:
			return ""
		if(database.db_check_user_exists(reciever)):
			get_user_points = database.db_get_user_points_int(self.user)
			if(int(amount) > get_user_points):
				return "You don't have {} {} {} FailFish".format(amount, CURRENCY, self.user)
			if(int(amount) <= 0):
				return ""
			else:
				database.db_add_points_user(reciever, amount)
				database.db_minus_points_user(self.user, amount)
				return "{} gave {} {} to {}! <3".format(self.user, amount, CURRENCY, reciever)
		else:
			return ""