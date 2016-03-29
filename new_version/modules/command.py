import logging, coloredlogs
from modules.config import *
from modules.database import Database
from modules.commandmanager import CommandManager
from modules.commandtext import commands, advanced_commands, api_commands
from modules.points import Points

class Command:

	def __init__(self, line, user):
		self.line = line
		self.user = user
		self.commands = commands
		self.advanced_commands = advanced_commands
		self.api_commands = api_commands
		self.points = Points(self.user)

	def return_command(self):
		try:
			command_check = CommandManager(self.line)
			parameter_2 = command_check.get_message_word(1).strip()
		except IndexError or NameError:
			parameter_2 = None
		try:
			command_check = CommandManager(self.line)
			parameter_3 = command_check.get_message_word(2).strip()
		except:
			parameter_3 = None

		for keys, values in self.commands.items():
			if keys in self.line:
				return self.text_command(keys, values, parameter_2, parameter_3)

		self.advanced_command(self.line, parameter_2, parameter_3)

		return ""

	def text_command(self, cmd, response, var2, var3):
		try:
			output = response.replace('<user>', self.user)
			if var2 is None:
				return output
			else:
				output = response.replace('<user>', self.user).replace('<param2>', var2)
				return output
		except:
			return response

	def advanced_command(self, cmd, var2, var3):
		print("commands >", self.advanced_commands)
		print("cmd={}=".format(cmd))

		if self.line in self.advanced_commands:
			print(True)
		else:
			print(False)

	# Return a basic text command
	# def text_command(self):
	# 	for keys, values in self.commands.items():
	# 		if keys in self.line:
	# 			try:
	# 				new_val = values.replace('<user>', self.user)
	# 				return new_val
	# 			except:
	# 				return values
	# 	return ""

	# def user_check_command(self):
	# 	for keys, values in self.advanced_commands.items():
	# 		try:
	# 			command_check = CommandManager(self.line)
	# 			parameter_2 = (command_check.get_message_word(1)).strip()
	# 		except IndexError or NameError:
	# 			parameter_2 = None

	# 		if keys in self.line:
	# 			if parameter_2 is None:
	# 				return values(self.user)
	# 			else:
	# 				# return self.points.roulette(parameter_2)
	# 				return values(parameter_2)
	# 	return ""

	# def api_command(self):
	# 	for keys, values in self.api_commands.items():
	# 		if keys in self.line:
	# 			return values()
	# 	return ""