import logging, coloredlogs
from modules.config import *
from modules.database import Database
from modules.commandmanager import CommandManager
from modules.commandtext import commands, advanced_commands, api_commands
from modules.points import Points
from modules.api import API
from modules.modules.time import Time
from modules.modules.playsound import PlaySound


database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Command:

	def __init__(self, line, user):
		self.line = line
		self.user = user
		self.commands = commands
		self.advanced_commands = advanced_commands
		self.api_commands = api_commands
		self.points = Points(self.user)
		self.time = Time()
		self.playsound = PlaySound(self.user)
		self.api = API(1)

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

		print("Message: {}".format(self.line))
		print("P2: {}".format(parameter_2))
		print("P3: {}".format(parameter_3))

		for keys, values in self.commands.items():
			if keys in self.line:
				print("Command found in text commands")
				return self.text_command(keys, values, parameter_2, parameter_3)

		for message in self.advanced_commands:
			if message in self.line.strip():
				print("Command found in advanced commands")
				return self.advanced_command(message, parameter_2, parameter_3)

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

	def advanced_command(self, line, var2, var3):
		if line == 'points':
			if var2 is None:
				print("return points {}".format(self.user))
				return database.db_get_points_user(self.user)
			else:
				return database.db_get_points_user(var2)
		if line == 'rank':
			if var2 is None:
				return database.db_get_user_rank(self.user)
			else:
				return database.db_get_user_rank(var2)
		if line == 'uptime':
			return self.time.uptime()
		if line == 'localtime':
			return self.time.local_time()
		if line == 'playsound':
			if var2 is None:
				return "{}, you didn't specify a sound. View them here {}".format(self.user, SOUNDS_LINK)
			else:
				return self.playsound.playsound(var2)
		if line == 'roulette':
			return self.points.roulette(var2)


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