import logging, coloredlogs

from modules.config import *
from modules.timer import Timer
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Points:

	CommandMain = ''
	CommandMainOptions = [CURRENCY, 'rank', 'give']
	CommandResponses = []

	def __init__(self, user, user_to_check):
		self.user = user
		self.currency = CURRENCY
		self.user_to_check = user_to_check
		# self.cooldown_timer = Timer(self.user, 120, RouletteCooldown, "Roulette")

	def execute_command(self, command):
		if command == Points.CommandMainOptions[0]:
			if self.user_to_check is None:
				self.get_user_points_self()
			else:
				self.get_user_points()
		if command == Points.CommandMainOptions[1]:
			if self.user_to_check is None:
				self.get_user_rank(self.user)
			else:
				self.get_user_rank(self.user_to_check)
		if command == Points.CommandMainOptions[2]:
			self.givepoints(self.user_to_check, self.user)

	def get_user_points_self(self):
		from modules.bot import bot_msg_whsp
		bot_msg_whsp(database.db_get_points_user(self.user, self.user), self.user)

	def get_user_points(self):
		from modules.bot import bot_msg
		bot_msg(database.db_get_points_user(self.user_to_check, self.user))

	def get_user_rank(self, user):
		from modules.bot import bot_msg
		bot_msg(database.db_get_user_rank(user))

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