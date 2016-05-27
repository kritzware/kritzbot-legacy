import logging, coloredlogs
from threading import Thread
from time import sleep

from modules.config import *
from modules.database import Database
from modules.commandmanager import CommandManager
from modules.commandtext import commands, advanced_commands
from modules.points import Points
from modules.api import API
# from modules.modules.time import Time
from modules.modules.playsound import PlaySound
from modules.modules.followalert import FollowAlert
from modules.modules.raffle import Raffle
from modules.modules.giveaway import Giveaway
from modules.modules.duel import Duel
from modules.modules.uptime import Uptime
from modules.modules.localtime import LocalTime
from modules.modules.adminpoints import AdminPoints
from modules.modules.AdminCommands import AdminCommands
from modules.modules.zoltar import Zoltar

from modules.Sockets.SongRequest import SongRequest

from modules.modules.showemote import ShowEmote

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Command:

	def __init__(self, line, user):
		self.line = line
		self.user = user
		self.command = self.line.split(" ")[0].strip()
		self.commands = commands
		self.advanced_commands = advanced_commands
		self.points = Points(self.user)
		# self.time = Time()
		self.playsound = PlaySound(self.user, PLAYSOUND_COST)
		self.followalert = FollowAlert('FollowAlert')
		self.api = API(1)

	def return_command(self):
		from modules.bot import bot_msg, bot_msg_raw
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

		# Text commands from database
		try:
		 	output = database.db_get_command(self.command, self.user)
		 	response = self.response_parse(output, parameter_2, parameter_3)
		 	bot_msg(response)
		 	return ""
		except:
		 	pass

		# Create advanced command objects
		command_objects = [Duel(self.user, parameter_2, parameter_3), 
						   Raffle(self.user, parameter_2, 10),
						   Uptime(),
						   LocalTime(),
						   AdminPoints(self.user, parameter_2, parameter_3),
						   AdminCommands(self.user, parameter_2, self.line.replace(parameter_2, '', 1).replace(self.command, '', 1)),
						   Zoltar(self.user, self.line),
						   SongRequest(self.user, parameter_2)
						  ]

		# Advanced commands
		for command_object in command_objects:
			try:
				if self.command == command_object.CommandMain or self.command in command_object.CommandMainOptions:
					print("{} command found".format(command_object.CommandMain))
					command_object.execute_command(self.command)
				if self.command in command_object.CommandResponses:
					print("{} command response found".format(self.command))
					command_object.execute_command_response(self.command)
			except:
				pass
		return ""

	def response_parse(self, response, variable_2, variable_3):
		try:
			output = response.replace('{x}', variable_2)
			if variable_3 is None:
				return output
			else:
				output = output.replace('{y}', variable_3)
				return output
		except:
			return response

	def advanced_command(self, cmd, var2, var3):
		from modules.bot import bot_msg, bot_msg_whsp

		if cmd == '{}'.format(CURRENCY):
			if var2 is None:
				bot_msg_whsp(database.db_get_points_user(self.user, self.user), self.user)
				return ""
			else:
				return database.db_get_points_user(var2, self.user)

		# if cmd == 'enter' and Giveaway.GiveawayActive and self.user not in Giveaway.GiveawayEntries:
		# 	Giveaway.GiveawayEntries.append(self.user)
		# 	return ""
		# if cmd == 'enter':
		# 	return ""

		if cmd == 'rank':
			if var2 is None:
				return database.db_get_user_rank(self.user)
			else:
				return database.db_get_user_rank(var2)
	
		if cmd == 'followage':
			self.api.get_follow_age(self.user)
			return ""

		# if cmd == 'playsound':
		# 	if var2 is None:
		# 		return "{}, you didn't specify a sound. View them here {}".format(self.user, SOUNDS_LINK)
		# 	else:
		# 		return self.playsound.playsound(var2)

		if cmd == 'tweet':
			self.api.get_latest_tweet()
			return ""

		if cmd == 'showemote':
			showemote = ShowEmote(self.user)
			return showemote.showemote(var2)

		if cmd == 'roulette':
			return self.points.roulette(var2)
		if cmd == 'give':
			if var2 is None or var3 is None:
				return ""
			else:
				return self.points.givepoints(var2, var3)
			
			# if cmd == 'giveaway':
			# 	command_text = self.line.replace(var2, '').replace(cmd, '')
			# 	giveaway = Giveaway(int(var2), command_text)
			# 	giveaway.start_giveaway()
			# 	return ""

		if cmd == 'test':
			bot_msg_whsp("{} viewers detected".format(len(self.api.get_viewers_json('viewers'))), ADMIN)
			return "Admin message sent to {}".format(ADMIN)
		# 	print("Raffle Active:", Raffle.RaffleActive)
		# 	print("Raffle Entries:", Raffle.RaffleEntries)
		# 	return ""
		# 	# return self.followalert.check_follower()
		# 	Thread(target=self.followalert.check_follower_run).start()
