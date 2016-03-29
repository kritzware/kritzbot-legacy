import logging, coloredlogs
from random import choice, randrange
from modules.database import Database
from modules.config import *

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Points:

	def __init__(self, user):
		self.user = user
		self.currency = CURRENCY

	def roulette(self, amount):
		gamble = randrange(1, 5)
		if(gamble == 1):
			total_win = int(amount) * 2
			database.db_add_points_user(self.user, total_win)
			output = "{} won {} {}! PogChamp".format(self.user, total_win, self.currency)
		else:
			database.db_minus_points_user(self.user, amount)
			output = "{} lost {} {}! BibleThump".format(self.user, amount, self.currency)
		print(output)
		return output