from time import gmtime, strftime

from kritzbot.logger import Logger
log = Logger(__name__)

class ChatStream:

	def __init__(self, message, user):
		self.msg = message
		self.user = user
		self.timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		self.msg_length = len(message)

	def parse(self):
		log.message(self.msg, self.msg_length, self.user)