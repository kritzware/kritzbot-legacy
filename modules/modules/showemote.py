import logging, coloredlogs
import json
import time

from threading import Thread
from modules.api import API
from modules.config import *
from modules.database import Database
from modules.timer import Timer
import os.path
import sys

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class ShowEmote:

	ShowEmoteCooldown = []

	def __init__(self, user):
		self.user = user

	def showemote(self, emote):
		self.add_emote_to_queue(emote, self.get_filepath())
		ShowEmoteTimerRun()
		return "Emote {} sent to queue".format(emote)

	def get_filepath(self):
		basepath = os.path.dirname(__file__)
		filepath = os.path.abspath(os.path.join(basepath, "..", "..", "..", "kritzwareio", "views", "emote_queue.json"))
		return filepath

	def add_emote_to_queue(self, emote, filepath):
		print(emote)
		with open(filepath, 'w'): pass
		with open(filepath, 'r+') as f:
			raw_data = '[{ "emote" : "' + emote + '" }]'
			parsed = json.loads(raw_data)
			print(parsed)
			f.seek(0)
			json.dump(parsed, f, indent=4)

EmoteQueue = ShowEmote('not_needed_must_remove')

class ShowEmoteTimer(Thread):

	def run(self):
		time.sleep(6)
		EmoteQueue.add_emote_to_queue('', EmoteQueue.get_filepath())

def ShowEmoteTimerRun():
	ShowEmoteTimer().start()