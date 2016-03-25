import logging, coloredlogs
from modules.api import API
from modules.timer import Timer

class Raffle:

	def __init__(self, user, points):
		self.user = user
		self.points = points

	def start_timer(self, time):
		print("raffle started, {}".format(points))
		raffle_timer_1 = Timer(int(time/2))
		raffle_timer.start()
		print("raffle half")
		raffle_timer_2 = Timer(int(time/2))
		raffle_timer.start()