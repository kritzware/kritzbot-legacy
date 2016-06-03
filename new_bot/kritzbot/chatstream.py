from time import gmtime, strftime

from kritzbot.commandmanager import CommandManager
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
		try:
			if(self.isCommand()):
				command = self.getCommand()
				command_handler = CommandManager(command, self.msg, self.user)
				command_handler.getCommand()
			else:
				self.nonCommand()
		except Exception as e:
			log.info(e)

	def isCommand(self):
		command_start = str(self.msg)[:1]
		if(command_start == '!'):
			return True
		return False

	def getCommand(self):
		cmd = self.msg.replace('!', '')
		return cmd

	def nonCommand(self):
		log.info('non command detected')
		# do non command stuff here 