import logging, coloredlogs
from threading import Thread

from modules.config import *
from modules.timer import Timer
from modules.api import API
from modules.database import Database

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class FollowAlert():

	def __init__(self, name):
		self.name = name

	def check_follower(self):
		latest_follower = database.db_get_follower()
		new_follower = ''
		