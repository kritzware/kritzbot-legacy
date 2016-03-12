import logging, coloredlogs

class Command:

	def __init__(self, line):
		self.line = line

	def check_line(self, line):
		if(self.line == 'Kappa'):
			return True
		else:
			return False

	def read_message(self):
		logging.info(self.line)
		if(self.check_line(self.line)):
			logging.info("command detected")
		else:
			logging.info("no command")