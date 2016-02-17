import string

from Read import getUser, getMessage
from TheSocket import openSocket, sendMessage
from Initialize import joinRoom
from Commands import commands

s = openSocket()
joinRoom(s)
readbuffer = ""

while True:
		readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			if "PING" in line:
				s.send(bytes(line.replace("PING", "PONG"), 'UTF-8'))
				break
			user = getUser(line)
			message = getMessage(line)
			print(user + " typed :" + message)
			if "!admin" in message:
				sendMessage(s, commands.get('admin'))
				break
			if "!test" in message:
				sendMessage(s, commands.get('test'))
				break