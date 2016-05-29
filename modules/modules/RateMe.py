import logging, coloredlogs
from threading import Thread
from random import choice

from modules.config import *
from modules.timer import Timer
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class RateMe:

	CommandMain = 'rateme'
	CommandMainOptions = []
	CommandResponses = []

	Cooldown = []
	Responses = [
					'You look a 0 out of 10 today @user 4Head',
					'Good job, you\'re finally a 1 out of 10 @user Keepo',
					'You seem a 2 out of 10 today, @user, going up in life? OpieOP',
					'A 3\'s a 3 @user, what can I say? ¯\_(ツ)_/¯',
					'A 4 out of 10 is slightly below average, good job @user SeemsGood',
					'Oh woooow, you got to a 5 out of 10 today @user! PogChamp Clap',
					'I\'m so proud of you, @user, you\'re a 6 out of 10 today KappaPride',
					'Lookin\' good, @user! You\'re a 7 out of 10 today! BCWarrior',
					'Well ain\'t you a looker, @user! Getting that 8 out of 10 today FeelCuteMan',
					'So close! You\'re a 9 out of 10 today @user \ MingLee /',
					'Holy shit! You\'re a 10 out of 10 today, @user! \ BabyRage / JUST TAKE MY MONEY!'
				]

	def __init__(self, user):
		self.user = user
		self.cooldown_timer = Timer(self.user, 3600, RateMe.Cooldown, "RateMe")

	def execute_command(self, command):
		if(self.user in self.cooldown_timer.timer_list):
			return ""
		else:
			self.rate_user()

	def rate_user(self):
		from modules.bot import bot_msg
		response = choice(RateMe.Responses)

		print(len(RateMe.Responses))

		if response == RateMe.Responses[10]:
			database.db_add_points_user(self.user, 30)

		output = self.parse_user(response)

		Thread(target=self.cooldown_timer.cooldown_run).start()
		bot_msg(output)

	def parse_user(self, string):
		return string.replace('@user', self.user)