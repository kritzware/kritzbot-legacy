from modules.temp import cooldown

from threading import Thread

import time


class cooldownTimer(Thread):

	def run(self):
		time.sleep(60)
		print("[INFO] >>> Removed from cooldown array user: {}".format(user))
		cooldown.remove(user)