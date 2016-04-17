import logging, coloredlogs
import json
import time
from threading import Thread
from modules.api import API
from modules.database import Database
from modules.config import *
from modules.timer import Timer
import os.path
import sys

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

PlaySoundCooldown = []

class PlaySound:

	def __init__(self, user, cost):
		self.user = user
		self.api = API(1)
		self.cost = cost
		self.available_sounds = ['beans', 'bs', 'concentration', 'swearjar', 'toohard', 'killinit', 'dammit', 'unbreakable']
		self.cooldown_timer = Timer(self.user, 900, PlaySoundCooldown, "PlaySound")

	def playsound(self, sound):
		if(self.user in self.cooldown_timer.timer_list):
			return ""
		else:
			if(sound in self.available_sounds):
				if(database.db_get_user_points_int(self.user) > self.cost):
					# Add sound to queue
					self.add_sound_to_queue(sound, self.get_filepath())

					# Minus points from user
					database.db_minus_points_user(self.user, self.cost)
					
					# Start cooldown timer thread
					Thread(target=self.cooldown_timer.cooldown_run).start()

					# Start timer to remove sound from JSON file
					PlaySoundTimerRun()
					return "{} just spent {} points on the audio clip {}!".format(self.user, self.cost, sound)
				else:
					return "{}, you don't have enough points FailFish".format(self.user)
			else:
				logging.warning("No sound specified by {}".format(self.user))
				return ""

	def get_filepath(self):
		basepath = os.path.dirname(__file__)
		filepath = os.path.abspath(os.path.join(basepath, "..", "..", "..", "..", "kritzwareio", "views", "queue.json"))
		return filepath

	def add_sound_to_queue(self, sound, filepath):
		print(sound)
		with open(filepath, 'w'): pass
		with open(filepath, 'r+') as f:
			raw_data = '[{ "sound" : "' + sound + '" }]'
			parsed = json.loads(raw_data)
			f.seek(0)
			json.dump(parsed, f, indent=4)

SoundQueue = PlaySound('not_needed_must_remove', 0)

class PlaySoundTimer(Thread):

	def run(self):
		time.sleep(4)
		SoundQueue.add_sound_to_queue('', SoundQueue.get_filepath())

def PlaySoundTimerRun():
 	PlaySoundTimer().start()