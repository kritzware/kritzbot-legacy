import logging, coloredlogs
from threading import Thread
import time
from random import choice

from modules.config import *
from modules.commandtext import auto_messages
from modules.database import Database
from modules.api import API

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Timer(Thread):

	def __init__(self, user, time, timer_list, name):
		# Seconds
		self.user = user
		self.time = time
		super(Timer, self).__init__()
		self.temp_message = ''
		self.timer_list = timer_list
		self.name = name
		self.api = API(1)
		
	def run(self):
		for viewers in self.api.get_viewers_json('viewers'):
			if database.db_check_user_exists(viewers) == False:
				database.db_add_user(viewers)
			database.db_add_points_user(viewers, VIEWER_POINT_GAIN) 

		for viewers in self.api.get_viewers_json('moderators'):
			if database.db_check_user_exists(viewers) == False:
				database.db_add_user(viewers)
			database.db_add_points_user(viewers, VIEWER_POINT_GAIN)

		time.sleep(self.time)
		self.auto()

	def auto(self):
		self.run()

	def auto_message(self):
		output = choice(auto_messages)
		print("OUT: ", output)
		self.temp_message = output
		print("TEMP: ", self.temp_message)
		self.get_message()
		time.sleep(self.time)
		self.auto_message_run()

	def get_message(self):
		return self.temp_message

	def cooldown(self):
		time.sleep(self.time)
		logging.info("{} removed from list {}".format(self.timer_list[0], self.name))
		self.timer_list.pop(0)

	def cooldown_run(self):
		self.timer_list.append(self.user)
		self.cooldown()