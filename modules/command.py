import logging, coloredlogs
from threading import Thread
from time import sleep

from modules.config import *
from modules.database import Database
from modules.commandmanager import CommandManager
from modules.commandtext import commands, advanced_commands
from modules.points import Points
from modules.api import API
from modules.modules.time import Time
from modules.modules.playsound import PlaySound
from modules.modules.followalert import FollowAlert
from modules.modules.raffle import Raffle

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
		self.time = Time()
		self.playsound = PlaySound(self.user, PLAYSOUND_COST)
		self.followalert = FollowAlert('FollowAlert')
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

		for keys, values in self.commands.items():
			if keys == self.command:
				return self.text_command(keys, values, parameter_2, parameter_3)

		# try:
		# 	output = database.db_get_command(self.command, self.user)
		# 	return output
		# except:
		# 	pass
		
		# try:
		# 	print(self.line)
		# 	return database.db_get_command(self.command, self.user)
		# except:
		# 	pass

		for message in self.advanced_commands:
			if message == self.command:
				return self.advanced_command(message, parameter_2, parameter_3)

		return ""

	# def text_command(self, cmd, var2, var3):
	# 	try:
	# 		output = cmd.replace('<user>', self.user)
	# 		if var2 is None:
	# 			return output
	# 		else:
	# 			output = cmd.replace('<user>', self.user).replace('<param2>', var2)
	# 			return output
	# 	except:
	# 		return cmd

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
		from modules.bot import bot_msg, bot_msg_whsp

		if cmd == 'points':
			if var2 is None:
				bot_msg_whsp(database.db_get_points_user(self.user, self.user), self.user)
				return ""
			else:
				return database.db_get_points_user(var2, self.user)
		if cmd == 'rank':
			if var2 is None:
				return database.db_get_user_rank(self.user)
			else:
				return database.db_get_user_rank(var2)
		if cmd == 'uptime':
			return self.time.uptime()
		if cmd == 'localtime':
			return self.time.local_time()
		if cmd == 'playsound':
			if var2 is None:
				return "{}, you didn't specify a sound. View them here {}".format(self.user, SOUNDS_LINK)
			else:
				return self.playsound.playsound(var2)
		if cmd == 'roulette':
			return self.points.roulette(var2)
		if cmd == 'give':
			if var2 is None or var3 is None:
				return ""
			else:
				return self.points.givepoints(var2, var3)


		
		# if cmd == 'duel':
		# 	if var2 is None or var3 is None:
		# 		return ""
		# 	else:
		# 		return self.points.duel(var2, var3)
		# if cmd == 'accept':
		# 	return self.points.duel_outcome(self.user)

		if cmd == 'songrequest':
			database.db_minus_points_user(self.user, 200)
			return ""

		# Moderator Commands
		if(self.api.check_user_class(self.user, 'moderators')):
			if cmd == 'raffle':
				raffle = Raffle(self.user, var2, 10)
				return raffle.start_raffle()

			# Add commands to Database
			if cmd == 'ac':
				if var2 is None or var3 is None:
					return ""
				else:
					command_text = self.line.replace(var2, '').replace(cmd, '')
					print(command_text)
					return database.db_add_command(var2, command_text)
			if cmd == 'ec':
				if var2 is None or var3 is None:
					return ""
				else:
					command_text = self.line.replace(var2, '').replace(cmd, '')
					print(command_text)
					return database.db_edit_command(var2, command_text)			
			if cmd == 'rc':
				if var2 is None:
					return ""
				else:
					return database.db_delete_command(var2)

		# Entry Keywords
		if cmd == 'join' and Raffle.RaffleActive and self.user not in Raffle.RaffleEntries:
			Raffle.RaffleEntries.append(self.user)
			bot_msg_whsp("You have successfully entered the raffle!", self.user)
			return ""
		if cmd == 'join':
			return ""

		if cmd == 'test':
			bot_msg_whsp("Whisper message", "kritzware")
			return ""
		# 	print("Raffle Active:", Raffle.RaffleActive)
		# 	print("Raffle Entries:", Raffle.RaffleEntries)
		# 	return ""
		# 	# return self.followalert.check_follower()
		# 	Thread(target=self.followalert.check_follower_run).start()