import logging, coloredlogs
from modules.config import *
from modules.database import Database
from modules.commandtext import commands, user_commands, advanced_commands

class Command:

	def __init__(self, line, user):
		self.line = line
		self.user = user
		self.commands = commands
		self.user_commands = user_commands
		self.advanced_commands = advanced_commands

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
				return values()
		return ""