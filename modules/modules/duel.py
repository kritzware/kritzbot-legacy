import logging, coloredlogs
from threading import Thread
from random import randrange

from modules.config import *
from modules.database import Database
from modules.timer import Timer

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Duel:

	DuelCooldown = []

	def __init__(self, user):
		self.user = user
		self.cooldown_timer = Timer(self.user, DUEL_COOLDOWN, Duel.DuelCooldown, "DuelCooldown")
		# opponent = opponent
		# amount = int(amount)

	def start_duel(self, opponent, amount):
		from modules.bot import bot_msg_whsp

		if(self.user in Duel.DuelCooldown):
			bot_msg_whsp("You can only start a duel every {} mins FailFish".format(int(DUEL_COOLDOWN/60)), self.user)
			return ""

		if(self.check(opponent, int(amount))):
			bot_msg_whsp("{} challenged you to a duel of {} {}! Reply with !accept/!reject in the main chat or wait {} mins for the duel to expire HotPokket".format(self.user, amount, CURRENCY, int(DUEL_EXPIRE/60)), opponent)
			bot_msg_whsp("You challenged {} to a duel of {} {}! If they don't respond within {} mins the duel will expire HotPokket".format(opponent, amount, CURRENCY, int(DUEL_EXPIRE/60)), self.user)
			# Add duel to the database
			database.db_add_duel(self.user, opponent, amount)
			# Start cooldown timer thread
			Thread(target=self.cooldown_timer.cooldown_run).start()
		else:
			return ""

	def check(self, opponent, amount):
		from modules.bot import bot_msg_whsp

		if(opponent == self.user):
			return False
		
		if(database.db_check_user_exists(self.user) == False or database.db_check_user_exists(opponent) == False):
			return False

		if(amount <= 0):
			return False

		user_points = database.db_get_user_points_int(self.user)
		opponent_points = database.db_get_user_points_int(opponent)

		if(amount > user_points):
			bot_msg_whsp("{}, you don't have {} {} FailFish".format(self.user, amount, CURRENCY), self.user)
			return False

		if(amount > opponent_points):
			bot_msg_whsp("{} doesn't have enough {} to accept this duel. Try a lower amount BabyRage".format(opponent, CURRENCY), self.user)
			return False

		if(self.check_status(opponent, amount)):
			return True
		else:
			return False

	def check_status(self, opponent, amount):
		from modules.bot import bot_msg_whsp

		if(database.db_check_duel_exists_user(self.user)):
			bot_msg_whsp("You are already in an active duel with {}.".format(database.db_get_duel_opponent_from_user(self.user)), self.user)
			return False

		if(database.db_check_duel_exists_opponent(opponent)):
			bot_msg_whsp("{} is already in an active duel.".format(opponent), self.user)
			return False

		if(database.db_check_duel_exists_opponent(self.user)):
			bot_msg_whsp("You must wait for your current duel with {} to finish before doing another.".format(database.db_get_duel_user_from_opponent(self.user)), self.user)
			return False

		return True

	def get_duel_win(self):
		from modules.bot import bot_msg, bot_msg_whsp
		if(database.db_check_duel_exists_opponent(self.user)):
			get_opponent = database.db_get_duel_user_from_opponent(self.user)
			win = randrange(0, 2)
			points_win = database.db_get_duel_amount(self.user)
			if(win == 0):
				print('win')
				bot_msg("{} won the duel against {} and gets {} {}! FeelsGoodMan KAPOW".format(self.user, get_opponent, points_win, CURRENCY))
				database.db_minus_points_user(get_opponent, points_win)
				database.db_add_points_user(self.user, points_win)
			else:
				print('win here')
				bot_msg("{} won the duel against {} and gets {} {}! FeelsGoodMan KAPOW".format(get_opponent, self.user, points_win, CURRENCY))
				database.db_minus_points_user(self.user, points_win)
				database.db_add_points_user(get_opponent, points_win)
			database.db_remove_duel(self.user)

	def cancel_duel(self):
		from modules.bot import bot_msg, bot_msg_whsp
		if(database.db_check_duel_exists_opponent(self.user)):
			get_opponent = database.db_get_duel_user_from_opponent(self.user)
			points_win = database.db_get_duel_amount(self.user)
			bot_msg("{} rejected the {} {} duel against {} BabyRage".format(self.user, points_win, CURRENCY, get_opponent))
			database.db_remove_duel(self.user)