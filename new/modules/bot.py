import socket
import string
import threading
import sys
import logging, coloredlogs

from modules.commands import Command

class Bot:

	def __init__(self, host, port, key, nick, channel):
		self.host = host
		self.port = port
		self.key = key
		self.nick = nick
		self.channel = channel

	def open_socket(self):
		try:
			s = socket.socket()
			s.connect((self.host, self.port))
			s.send(bytes("PASS {} \r\n".format(self.key), 'UTF-8'))
			s.send(bytes("NICK {} \r\n".format(self.nick), 'UTF-8'))
			s.send(bytes("JOIN #{} \r\n".format(self.channel), 'UTF-8'))
			logging.info("Connecting to TWITCH IRC..")
			return s
		except socket.error as e:
			print(e)
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
			global command
			command = Command(message)
			return message
		else:
			logging.error("No data from server")

	def pong(self, s, line):
		if "PING :tmi.twitch.tv" in line:
			# print("[INFO] PING RECIEVED")
			response = "PING :tmi.twitch.tv\r\n"
			# print(response)
			bytes_response = str.encode(response)
			s.send(bytes_response)
			logging.info("PING request : PONG sent")
			return True
		else:
			return False

	def send_message(self, s, message):
		temp_message = "PRIVMSG # {} : {}".format(self.channel, message)
		s.send(bytes("{}\r\n".format(temp_message), 'UTF-8'))
		logging.info("Bot sent: {}".format(message))

	def connection(self):
		s = self.open_socket()
		self.join_channel(s)
		readbuffer = ""
		while True:
			readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
			temp = str.split(readbuffer, "\n")
			readbuffer = temp.pop()
			for line in temp:
				# print(line)
				if(self.pong(s, line)):
					break
				user = self.get_user(line)
				message = self.get_message(line)
				logging.info("{}: {}".format(user, message))
				
				command.read_message()