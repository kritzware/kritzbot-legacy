import string
import threading

# external py files
from modules.irc_socket import sendMessage
from modules.sql import db_add_points_global
from modules.basic_commands import chat_auto_messages

version = "version 1.2"

def joinRoom(s):

	readbuffer = ""
	loading = True
	while loading:

		readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for line in temp:
			print(line)
			loading = loadingComplete(line)

	# sends message on join
	# sendMessage(s, " joined the channel, running on {} [DEV]".format(version))

	# def auto_message():
	# 	threading.Timer(600, auto_message).start()
	# 	sendMessage(s, chat_auto_messages())
	# auto_message()

	def points_timer():
		threading.Timer(60, points_timer).start()
		db_add_points_global(2)
	points_timer()

def loadingComplete(line):

	if("End of /NAMES list" in line):
		return False
	else:
		return True