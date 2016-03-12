import logging, coloredlogs

class CommandManager:

	def __init__(self, line):
		self.line = str(line)

	def check_line(self, line):
		command_start = line[:1]
		if(command_start == '!'):
			return True
		else:
			return False

	def parse_message(self, line):
			return line[1:]