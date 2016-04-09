import socket
import string
import sys
import logging, coloredlogs
from threading import Thread

from modules.commandmanager import CommandManager
from modules.command import Command
from modules.timer import Timer

class Bot:

	def __init__(self, host, port, key, nick, channel):
		self.host = host
		self.port = port
		self.key = key
		self.nick = nick
		self.channel = channel
		self.points_timer = Timer("not_needed_here", 120, [], "ViewerTimer")

	def open_socket(self):
		try:
			s = socket.socket()
			s.connect((self.host, self.port))
			s.send(bytes("PASS {} \r\n".format(self.key), 'UTF-8'))
			s.send(bytes("NICK {} \r\n".format(self.nick), 'UTF-8'))
			s.send(bytes("JOIN #{} \r\n".format(self.channel), 'UTF-8'))
			# s.send(bytes("CAP REQ :twitch.tv/commands", 'UTF-8'))
			# s.send(bytes("CAP REQ :twitch.tv/tags", 'UTF-8'))
			logging.info("Connecting to TWITCH IRC..")
			return s
		except socket.error as e:
			logging.error(e)
			sys.exit(1)

	def join_channel(self, s):
		logging.info("Joining channel: #{}".format(self.channel))
		readbuffer = ""
		loading = True
		while loading:
			readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
			temp = str.split(readbuffer, "\n")
			readbuffer = temp.pop()
			for line in temp:
				loading = self.loading_complete(line)

	def loading_complete(self, line):
		if("End of /NAMES list" in line):
			return False
		else:
			return True

	def get_user(self, line):
		if line != "":
			seperate = line.split(":", 2)
			user = seperate[1].split("!", 1)[0]
			return user
		else:
			logging.error("No data from server")

	def get_message(self, line):
		if line != "":
			seperate = line.split(":", 2)
			message = seperate[2]
			global command_check
			command_check = CommandManager(message)
			return message
		else:
			logging.error("No data from server")

	def pong(self, s, line):
		if "PING :tmi.twitch.tv" in line:
			response = "PING :tmi.twitch.tv\r\n"
			bytes_response = str.encode(response)
			s.send(bytes_response)
			logging.info("PING request : PONG sent")
			return True
		else:
			return False

	def send_message(self, s, message):
		temp_message = "PRIVMSG #{} : {}".format(self.channel, message)
		s.send(bytes("{}\r\n".format(temp_message), 'UTF-8'))
		if(message == ""):
			return
		else:
			logging.warning("> {}".format(message))

	def bot_commands(self, user, message):
		if(command_check.check_line(message)):
			parse_command = command_check.parse_message(message)
			command = Command(parse_command, user)
			try:
				self.send_message(server_connection, command.return_command())
				# self.send_message(server_connection, command.text_command())
				# self.send_message(server_connection, command.user_check_command())
				# self.send_message(server_connection, command.api_command())
			except:
				pass

	def connection(self):
		global server_connection
		server_connection = self.open_socket()
		self.join_channel(server_connection)
		readbuffer = ""

		# Announce to chat upon joining channel
		# self.send_message(server_connection, "starting up (dev version 1.1.5) MrDestructoid")

		# Start auto message thread
		Thread(target=self.points_timer.auto).start()

		while True:
			readbuffer = readbuffer + server_connection.recv(1024).decode('UTF-8')
			temp = str.split(readbuffer, "\n")
			readbuffer = temp.pop()
			for line in temp:
				# print(line)
				if(self.pong(server_connection, line)):
					break
				user = self.get_user(line)
				return_user(user)
				message = self.get_message(line)
				logging.info("{}: {}".format(user, message))
				self.bot_commands(user, message)

def return_user(chatter):
	return chatter