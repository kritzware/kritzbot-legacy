import logging, coloredlogs
import json
import urllib.request
from datetime import datetime, timedelta, date, time

from modules.config import CHANNEL

class API:

	def __init__(self, input):
		self.input = input

	def getJSON(self, url):
		request = urllib.request.urlopen(url)
		data = json.loads(request.read().decode('UTF-8'))
		return data

	def check_stream_online(self):
		try:
			data = self.getJSON('https://api.twitch.tv/kraken/streams?channel={}'.format(CHANNEL))
			online = int(data['_total'])
			print(online)
			if(online == 1):
				return True
			else:
				return False
		except urllib.error.URLError as e:
			logging.warning("Error: No connection to TWITCH API")

	def check_user_class(self, user, user_class):
		try:
			data = self.getJSON('https://tmi.twitch.tv/group/user/{}/chatters'.format(CHANNEL))
			chatters = data['chatters'][user_class]
			for n in chatters:
				if(n == user):
					return True
		except urllib.error.URLError as e:
			logging.warning("Error: TWITCH API connection")

test = API(1)
test.check_stream_online()