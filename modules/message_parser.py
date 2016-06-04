import logging, coloredlogs
from time import gmtime, strftime

from modules.config import *
from modules.api import API

class MessageParser:

	def __init__(self, message, user):
		self.message = message
		self.user = user
		self.timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		self.message_length = len(message)
		self.api = API(1)

	def start_parse(self):
		logging.info("[{}]({}) {}: {}".format(self.timestamp, self.message_length, self.user, self.message))
		self.spam_protection()
		# self.link_checker

	def spam_protection(self):
		from modules.bot import bot_msg_raw, bot_msg_whsp
		if(self.message_length > MESSAGE_LENGTH_TIMEOUT):
			if(self.api.check_user_class(self.user, 'moderators') == False):
				bot_msg_raw('/timeout {} {}'.format(self.user, MESSAGE_TIMEOUT_LENGTH))
				bot_msg_whsp('You have been timed out for {} secs because your message was to large FailFish'.format(MESSAGE_TIMEOUT_LENGTH), self.user)
				logging.info('Timeout for user: {}'.format(self.user))