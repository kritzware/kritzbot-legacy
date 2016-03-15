from threading import Thread
import time

from modules.database import database

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

	def run(self):
		time.sleep(5)
		print("adding points")
		time.sleep(5)
		print("points added")