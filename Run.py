import string
import re

from Read import getUser, getMessage, uptime, get_points, localtime, roulette
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

			

			# advanced commands
			if "!uptime" in message:
				#uptime()
				sendMessage(s, uptime())
			if "!localtime" in message:
				sendMessage(s, localtime())
			if "!points" in message:
				sendMessage(s, get_points(user))

			# roulette
			amount = re.findall('\d+', message)
			x = str(amount)
			if ("!roulette") in message:
				sendMessage(s, roulette(user, x))

			# basic commands
			if "!admin" in message:
				sendMessage(s, commands.get('admin'))
				break
			if "!commands" in message or "!help" in message:
				sendMessage(s, user + commands.get('commands'))
				break
			if "!twitter" in message:
				sendMessage(s, commands.get('twitter'))
			if "!discord" in message:
				sendMessage(s, commands.get('discord'))
			if "!spooky" in message:
				sendMessage(s, commands.get('spooky'))
			if "!coloring" in message:
				sendMessage(s, commands.get('coloring'))