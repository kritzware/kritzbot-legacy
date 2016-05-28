import logging, coloredlogs
import tweepy

from modules.config import *

class Twitter:

	CommandMain = ''
	CommandMainOptions = ['tweet']
	CommandResponse = []

	def __init__(self, user):
		self.user = user

	def execute_command(self, command):
		if command == Twitter.CommandMainOptions[0]:
			self.get_latest_tweet()

	def get_latest_tweet(self):
		from modules.bot import bot_msg
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		api = tweepy.API(auth)
		parsed_user = TWITTER[12:]
		tweet = api.user_timeline(id = parsed_user, count = 1)[0]
		content = tweet.text
		bot_msg("Latest tweet from {}: {}".format(CHANNEL, content))