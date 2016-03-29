import logging, coloredlogs
from threading import Thread
import time
from random import choice

from modules.commandtext import auto_messages
# from modules.database import database

# class Timer:

# 	def __init__(self, time):
# 		self.time = time

# 	def start_timer(self):
# 		print("timer started")
# 		threading.Timer(self.time, self.action()).start()

# 	def action(self):
# 		print("adding points")
# 		database.db_add_points_user("kritzware", 100)

class Timer(Thread):

	def __init__(self, time):
		self.time = time
		super(Timer, self).__init__()
		self.temp_message = ''

	def run(self):
		half_time = int(self.time) / 2
		time.sleep(half_time)
		print("adding points")
		time.sleep(half_time)
		print("points added")
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

	def auto_message_run(self):
		self.auto_message()

	def get_message(self):
		return self.temp_message