import logging
import coloredlogs

coloredlogs.install()

class Logger:

	def __init__(self, __name__):
		self.name = __name__
		logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)", "%Y-%m-%d %H:%M:%S")
		self.log = logging.getLogger(self.name)
		
	def info(self, message):
		self.log.setLevel(logging.INFO)
		self.log.info(message)

	def debug(self, message):
		self.log.setLevel(logging.DEBUG)
		self.log.debug(message)

	def message(self, message, msg_length, user):
		self.log.setLevel(logging.INFO)
		self.log.info('[MSG]({}) {}: {}'.format(msg_length, user, message))