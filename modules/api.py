import logging, coloredlogs
import json
import tweepy
import urllib.request
from datetime import datetime, timedelta, date, time

from modules.config import *

class API:

	def __init__(self, input):
		self.input = input

	def getJSON(self, url):
		try:
			request = urllib.request.urlopen(url)
			data = json.loads(request.read().decode('UTF-8'))
			return data
		except urllib.error.URLError as e:
			logging.warning("Error: TWITCH API connection")

	def check_stream_online(self):
		data = self.getJSON('https://api.twitch.tv/kraken/streams?channel={}'.format(CHANNEL))
		online = int(data['_total'])
		if(online == 1):
			return True
		else:
			return False

	def check_user_class(self, user, user_class):
		data = self.getJSON('https://tmi.twitch.tv/group/user/{}/chatters'.format(CHANNEL))
		chatters = data['chatters'][user_class]
		if user in chatters:
			return True
		return False

	def get_viewers_json(self, user_class):
		data = self.getJSON('https://tmi.twitch.tv/group/user/{}/chatters'.format(CHANNEL))
		chatters = data['chatters'][user_class]
		return chatters

	def get_latest_highlight(self, info):
		data = self.getJSON('https://api.twitch.tv/kraken/channels/{}/videos?limit=1'.format(CHANNEL))
		return_data = data['videos'][0][info]
		return return_data

	def get_latest_follower(self):
		data = self.getJSON('https://api.twitch.tv/kraken/channels/{}/follows?limit=1'.format(CHANNEL))
		return_data = data['follows'][0]['user']['name']
		return return_data

	def get_latest_tweet(self):
		from modules.bot import bot_msg
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		api = tweepy.API(auth)
		parsed_user = TWITTER[12:]
		tweet = api.user_timeline(id = parsed_user, count = 1)[0]
		content = tweet.text
		bot_msg("Latest tweet from {}: {}".format(CHANNEL, content))