import logging, coloredlogs
from threading import Thread
from time import sleep

from modules.config import *
from modules.timer import Timer
from modules.api import API
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

LatestFollower = ''
FollowMessage = "Thanks for following {}! PogChamp PogChamp".format(LatestFollower)

class FollowAlert():

	def __init__(self, name):
		self.name = name
		self.api = API(1)
		self.LatestFollower = ''
		self.FollowMessage = "Thanks for following {}! PogChamp PogChamp".format(self.LatestFollower)

	def check_follower(self):
		latest_follower = database.db_get_follower()
		new_follower = self.get_latest_follower()

		if(latest_follower != new_follower):
			database.db_new_follower(new_follower)
			print("new follower found")
			self.LatestFollower = new_follower
			sleep(5)
			self.check_follower_run()
		else:
			print("checking again")
			sleep(5)
			self.check_follower_run()

	def get_latest_follower(self):
		return self.api.get_latest_follower()

	def check_follower_run(self):
		self.check_follower()