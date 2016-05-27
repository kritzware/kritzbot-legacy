import logging, coloredlogs

from modules.config import *
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class AdminPoints:

	CommandMain = ''
	CommandMainOptions = ['add', 'minus']
	CommandResponses = []

	def __init__(self, user, recipient, amount):

		self.user = user
		self.recipient = recipient
		self.amount = amount


	def execute_command(self, command):
		if(self.user == ADMIN or self.user == CHANNEL):
			if command == AdminPoints.CommandMainOptions[0]:
				self.add()
			if command == AdminPoints.CommandMainOptions[1]:
				self.minus()

	def add(self):
		from modules.bot import bot_msg
		database.db_add_points_user(self.recipient, self.amount)
		bot_msg("An admin gave {} {} {} DatSheffy".format(self.recipient, self.amount, CURRENCY))

	def minus(self):
		from modules.bot import bot_msg
		database.db_minus_points_user(self.recipient, self.amount)
		bot_msg("An admin took {} {} from {} DatSheffy".format(self.amount, CURRENCY, self.recipient))