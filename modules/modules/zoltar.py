import logging, coloredlogs
from threading import Thread
from random import choice

from modules.config import *
from modules.database import Database
from modules.timer import Timer

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Zoltar:

	CommandMain = 'zoltar'
	CommandMainOptions = []
	CommandResponses = []

	ZoltarCooldown = []

	def __init__(self, user, question):
		self.user = user
		self.cooldown_timer = Timer(self.user, ZOLTAR_COOLDOWN, Zoltar.ZoltarCooldown, "ZoltarCooldown")
		self.minutes = int(ZOLTAR_COOLDOWN / 60)
		self.question = question
		self.responses = [
						'it is certain',
						'it is decidedly so',
						'without a doubt',
						'yes, definitely',
						'you may rely on it',
						'as I see it, yes',
						'most likely',
						'outlook good',
						'yes',
						'signs point to yes',
						'better not tell you now',
						'cannot predict now',
						'don\'t count on it',
						'my reply is no',
						'my sources say no',
						'outlook not so good',
						'very doubtful',
						 ]

	def execute_command(self, command):
		if(self.user not in Zoltar.ZoltarCooldown):
			self.prediction()

	def prediction(self):
		from modules.bot import bot_msg
		response = choice(self.responses)
		bot_msg("Zoltar takes {} of your {} and looks into the crystal ball.. he responds, \"{} {}\" deIlluminati".format(ZOLTAR_COST, CURRENCY, response, self.user))
		database.db_minus_points_user(self.user, ZOLTAR_COST)
		Thread(target=self.cooldown_timer.cooldown_run).start()