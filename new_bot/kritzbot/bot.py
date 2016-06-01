import socket
import os, sys
import string

from kritzbot.chatstream import ChatStream
from kritzbot.logger import Logger
log = Logger(__name__)

class Bot:

	def __init__(self, host, port, key, nick, channel):
		self.host  	 = host
		self.port 	 = port
		self.key  	 = key
		self.nick 	 = nick
		self.channel = channel

	def openSocket(self):
		try:
			s = socket.socket()
			s.connect((self.host, self.port))
			s.send(bytes("PASS {} \r\n".format(self.key), 'UTF-8'))
			s.send(bytes("NICK {} \r\n".format(self.nick), 'UTF-8'))
			s.send(bytes("JOIN #{} \r\n".format(self.channel), 'UTF-8'))
			s.send(bytes("CAP REQ :twitch.tv/membership", 'UTF-8'))
			s.send(bytes("CAP REQ :twitch.tv/commands", 'UTF-8'))
			s.send(bytes("CAP REQ :twitch.tv/tags", 'UTF-8'))
			log.info('Creating connection to #{}..'.format(self.channel))
			return s
		except socket.error as e:
			sys.exit(1)

	def joinChannel(self, s):
		readbuffer = ""
		loading = True
		log.info('Attempting to join channel #{}..'.format(self.channel))
		while loading:
			readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
			temp = str.split(readbuffer, '\n')
			readbuffer = temp.pop()
			for line in temp:
				loading = self.loadingComplete(line)

	def loadingComplete(self, line):
		if("End of /NAMES list" in line):
			return False
		return True

	def getUser(self, line):
		if line != '':
			seperate = line.split(':', 2)
			user = seperate[1].split('!', 1)[0]
			return user

	def getMessage(self, line):
		if line != '':
			seperate = line.split(':', 2)
			message = seperate[2]
			return message

	def sendMessage(self, s, message):
		temp_message = "PRIVMSG #{} : {}".format(self.channel, message)
		s.send(bytes('{}\r\n'.format(temp_message), 'UTF-8'))

	def pong(self, s, line):
		if 'PING :tmi.twitch.tv' in line:
			response = 'PONG :tmi.twitch.tv\r\n'
			bytes_response = str.encode(response)
			s.send(bytes_response)
			return True
		return False

	def connectChannel(self):
		server_connection = self.openSocket()
		self.joinChannel(server_connection)
		readbuffer = ''
		log.info('Successfully joined #{} - Hello world!'.format(self.channel))
		
		self.sendMessage(server_connection, 'hidden')
		self.sendMessage(server_connection, 'joined channel, running version 4: LUL')

		while True:
			readbuffer = readbuffer + server_connection.recv(1024).decode('UTF-8')
			temp = str.split(readbuffer, '\n')
			readbuffer = temp.pop()
			for line in temp:
				if(self.pong(server_connection, line)):
					break
				
				

				user = self.getUser(line)
				message = self.getMessage(line)
				
				try:
					chat_stream = ChatStream(message, user)
					chat_stream.parse()
				except Exception as e:
					log.info(e)