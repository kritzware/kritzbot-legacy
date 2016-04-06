import json
import time
from threading import Thread
from modules.api import API
from modules.database import Database
from modules.config import *
import os.path
import sys

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class PlaySound:

	def __init__(self, user, cost):
		self.user = user
		self.api = API(1)
		self.cost = cost

	def playsound(self, sound):
		self.add_sound_to_queue(sound, self.get_filepath())
		# self.start_timer()
		PlaySoundTimerRun()
		database.db_minus_points_user(self.user, self.cost)
		return "{} just spent {} points on an audio clip!".format(self.user, self.cost)

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

		# with open(filepath, 'r+') as f:
		# 	data = json.load(f)
		# 	print("original:", data[0]['sound'])
		# 	data[0]['sound'] = sound
		# 	print("altered:", data[0]['sound'])
		# 	f.seek(0)
		# 	json.dump(data, f, indent=4)

	# def run(self):
	# 	print("timer started")
	# 	time.sleep(5)
	# 	self.add_sound_to_queue('', self.get_filepath())
	# 	print("timer finished")

	# def start_timer(self):
	# 	self.run().start()

SoundQueue = PlaySound('not_needed_must_remove', 0)

class PlaySoundTimer(Thread):

	def run(self):
		time.sleep(10)
		SoundQueue.add_sound_to_queue('', SoundQueue.get_filepath())

def PlaySoundTimerRun():
 	PlaySoundTimer().start()