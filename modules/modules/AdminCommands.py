import logging, coloredlogs

from modules.config import *
from modules.database import Database
from modules.api import API

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class AdminCommands:

	CommandMain = ''
	CommandMainOptions = ['ac', 'ec', 'rc']
	CommandResponses = []

	def __init__(self, user, command, content):
		self.user = user
		self.command = command
		self.content = content
		self.api = API(1)

	def execute_command(self, command):
		if(self.api.check_user_class(self.user, 'moderators')):
			if command == AdminCommands.CommandMainOptions[0]:
				self.add_command()
			if command == AdminCommands.CommandMainOptions[1]:
				self.edit_command()
			if command == AdminCommands.CommandMainOptions[2]:
				self.remove_command()

	def add_command(self):
		from modules.bot import bot_msg_whsp
		if(database.db_add_command(self.command, self.content, self.user)):
			logging.info(self.command_log())
			bot_msg_whsp("Command !{} was added to the database SeemsGood".format(self.command), self.user)
		else:
			bot_msg_whsp("Error: Command {} already exists OMGScoots".format(command), self.user)

	def edit_command(self):
		from modules.bot import bot_msg_whsp
		if(database.db_edit_command(self.command, self.content, self.user)):
			logging.info(self.command_log())
			bot_msg_whsp("Command !{} was successfully updated to {}".format(self.command, self.content), self.user)
		else:
			bot_msg_whsp("Error: Command {} doesn't exist OMGScoots".format(self.command), self.user)

	def remove_command(self):
		from modules.bot import bot_msg_whsp
		if(database.db_delete_command(self.command, self.user)):
			logging.info(self.command_log())
			bot_msg_whsp("Command !{} was successfully deleted KAPOW".format(self.command), self.user)
		else:
			bot_msg_whsp("Error: Command {} doesn't exist OMGScoots".format(self.command), self.user)

	def command_log(self):
		return "{} modified command: {}".format(self.user, self.command)