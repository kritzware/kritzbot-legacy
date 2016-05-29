import logging, coloredlogs
from threading import Thread
from random import randrange

from modules.config import *
from modules.timer import Timer
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Roulette:

	CommandMain = 'roulette'
	CommandMainOptions = []
	CommandResponses = []

	RouletteCooldown = []

	def __init__(self, user, amount):
		self.user = user
		self.currency = CURRENCY
		self.amount = amount
		self.cooldown_timer = Timer(self.user, 120, Roulette.RouletteCooldown, "Roulette")

	def execute_command(self, command):
		if(self.user in self.cooldown_timer.timer_list):
			return ""
		else:
			self.roulette(self.amount)

	def roulette(self, amount):
		from modules.bot import bot_msg, bot_msg_whsp
		get_user_points = database.db_get_user_points_int(self.user)
		if(int(amount) > get_user_points):
			bot_msg_whsp("You don't have {} {} {} FailFish".format(amount, CURRENCY, self.user), self.user)
			return ""
		if(int(amount) <= 0):
			return ""
		gamble = randrange(1, 3)
		if(gamble == 1):
			total_win = int(amount) * 2
			database.db_add_points_user(self.user, total_win)
			output = "{} won {} {}! PogChamp".format(self.user, total_win, self.currency)
		else:
			database.db_minus_points_user(self.user, amount)
			output = "{} lost {} {}! BibleThump".format(self.user, amount, self.currency)
		Thread(target=self.cooldown_timer.cooldown_run).start()
		bot_msg(output)