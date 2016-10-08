import logging, coloredlogs
import tweepy
from urllib.request import Request, urlopen

from modules.config import *
from modules.api import API

class FollowAge:

	CommandMain = 'followage'
	CommandMainOptions = []
	CommandResponse = []

	def __init__(self, user, user_to_check):
		self.user = user
		self.user_to_check = user_to_check
		self.api = API(1)

	def execute_command(self, command):
		if self.user_to_check is None:
			self.get_follow_age(self.user)
		else:
			self.get_follow_age(self.user_to_check)

	def get_follow_age(self, follower):
		from modules.bot import bot_msg
		follow_age_raw = self.api.getRawHTML('https://api.rtainc.co/twitch/channels/{}/followers/{}'.format(CHANNEL, follower))
		if(str(follow_age_raw) == "{} isn't following {}".format(follower, CHANNEL)):
			bot_msg("{} isn't following the channel! FeelsBadMan".format(follower))
		else:
			bot_msg("{}! FeelsGoodMan".format(follow_age_raw))