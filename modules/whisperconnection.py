import socket
import string
import threading
import sys
import time
import logging, coloredlogs

class WhisperConnection:

	def __init__(self, host, port, key, nick, channel):
		self.host = host
		self.port = port
		self.key = key
		self.nick = nick
		self.channel = channel

	def open_whisper_socket(self):
		try:
			w = socket.socket()
			w.connect((self.host, self.port))
			w.send(bytes("PASS {} \r\n".format(self.key), 'UTF-8'))
			w.send(bytes("NICK {} \r\n".format(self.nick), 'UTF-8'))
			w.send(bytes("JOIN #{} \r\n".format(self.channel), 'UTF-8'))
			w.send(bytes("CAP REQ :twitch.tv/commands", 'UTF-8'))
			w.send(bytes("CAP REQ :twitch.tv/tags", 'UTF-8'))
			logging.info("Connecting to TWITCH IRC Whisper server..")
			return w
		except socket.error as e:
			logging.error(e)
			sys.exit(1)

	def join_group_channel(self, w):
		logging.info("Joining group channel #{}".format(self.channel))
		readbuffer = ""
		loading = True
		while loading:
			readbuffer = readbuffer + w.recv(1024).decode('UTF-8')
			temp = str.split(readbuffer, "\n")
			readbuffer = temp.pop()
			for line in temp:
				print(line)
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
			return message
		else:
			logging.error("No data from server")

	def pong(self, w, line):
		if "PING :tmi.twitch.tv" in line:
			# print("[INFO] PING RECIEVED")
			response = "PING :tmi.twitch.tv\r\n"
			# print(response)
			bytes_response = str.encode(response)
			w.send(bytes_response)
			logging.info("GROUP PING request : GROUP PONG sent")
			return True
		else:
			return False

	def send_whisper(self, w, user, message):
		temp_message = "PRIVMSG #jtv :/w {} {}".format(user, message)
		w.send(bytes("{}\r\n".format(temp_message), 'UTF-8'))
		logging.info("Bot sent whisper: {}".format(message))

	def connection(self):
		w = self.open_whisper_socket()
		self.join_group_channel(w)
		readbuffer = ""
		while True:
			print("Starting connection")
			time.sleep(60)
			readbuffer = readbuffer + w.recv(1024).decode('UTF-8')
			print("Connected!")
			temp = str.split(readbuffer, "\n")
			readbuffer = temp.pop()
			for line in temp:
				
				if(self.pong(w, line)):
					break
				user = self.get_user(line)
				message = self.get_message(line)
				
				logging.info("{}: {}".format(user, message))

				if message == 'send':
					send_whisper(w, user, 'whisper message')