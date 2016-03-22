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
		half_time = int(self.time) / 2
		time.sleep(half_time)
		print("adding points")
		time.sleep(half_time)
		print("points added")
		self.auto()

	def auto(self):
		self.run()