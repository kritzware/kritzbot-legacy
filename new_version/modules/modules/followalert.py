import logging, coloredlogs
from threading import Thread
from time import sleep

from modules.config import *
from modules.timer import Timer
from modules.api import API
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class FollowAlert():

	def __init__(self, name):
		self.name = name
		self.api = API(1)

	def check_follower(self):
		latest_follower = database.db_get_follower()
		new_follower = self.get_latest_follower()

		if(latest_follower != new_follower):
			database.db_new_follower(new_follower)
			try:
				return "Thanks for following {}! PogChamp PogChamp".format(new_follower)
			finally:
				sleep(5)
				self.check_follower_run()
		else:
			try:
				return "No new follower found MVGame"
			finally:
				print("checking again")
				sleep(5)
				self.check_follower_run()

	def get_latest_follower(self):
		return self.api.get_latest_follower()

	def check_follower_run(self):
		self.check_follower()