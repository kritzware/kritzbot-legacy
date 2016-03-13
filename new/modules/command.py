import logging, coloredlogs
from modules.config import *
from modules.database import Database
from modules.commandtext import commands, user_commands, advanced_commands
from modules.commandmanager import CommandManager

class Command:

	def __init__(self, line, user):
		self.line = line
		self.user = user
		self.commands = commands
		self.user_commands = user_commands
		self.advanced_commands = advanced_commands
		try:
			command_check = CommandManager(self.line)
			self.parameter_2 = command_check.get_message_word(1)
			self.parameter_3 = command_check.get_message_word(2)
		except Exception:
			pass

	def basic_command(self):
		for keys, values in self.commands.items():
			if keys in self.line:
				return values
		return ""

	def user_command(self):
 		for keys, values in self.user_commands.items():
 			if keys in self.line:
 				output = "{}{}".format(self.user, values)
 				return output
 		return ""

	def advanced_command(self):
		for keys, values in self.advanced_commands.items():
			if keys in self.line:
				return values(self.user)
		return ""