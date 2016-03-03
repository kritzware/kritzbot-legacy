import string
import threading

# external py files
from modules.irc_socket import sendMessage
from modules.sql import db_add_points_global, db_add_points_user, db_check_user
from modules.basic_commands import chat_auto_messages
from modules.api import get_users_json_viewers, get_users_json_mods

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
		try:
			viewers_chat = get_users_json_viewers()
			mods_chat = get_users_json_mods()
			for n in viewers_chat:
				if(db_check_user(n)):
					db_add_points_user(n, 2)
					print("[DEBUG] >>> {} earned 2 points".format(n))
			for n in mods_chat:
				if(db_check_user(n)):
					db_add_points_user(n, 2)
					print("[DEBUG] >>> {} earned 2 points".format(n))
		except Exception as e:
			print(e)

	points_timer()

def loadingComplete(line):

	if("End of /NAMES list" in line):
		return False
	else:
		return True