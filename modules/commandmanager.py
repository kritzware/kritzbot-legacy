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
		#cmd = self.get_message_word(0).replace('!', '')
		# line[1:]
		cmd = line.replace('!', '')
		return cmd

	def get_message_word(self, n):
		return self.line.split(" ")[n]