import threading

# external py files
from bot import (get_user,
	get_message,
	local_time,
	basic_command,
	update_command)
from irc_socket import openSocket, sendMessage
from irc_init import joinRoom
from sql import (db_add_user,
	db_add_points_user,
	db_minus_points_user,
	db_add_points_global,
	db_check_user,
	db_get_points_user,
	db_get_points_user_first)

# connection to the irc server is created
s = openSocket()
joinRoom(s)
readbuffer = ""

while True:

		readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)

			if "PING :tmi.twitch.tv" in line:
				response = "PONG :tmi.twitch.tv\r\n"
				print(response)
				bytes_response = str.encode(response)
				s.send(bytes_response)
				break
			user = get_user(line)
			message = get_message(line)
			print(user + " typed :" + message)

			#### POINT BASED COMMANDS ###

			# returns how many points a user owns
			if "!points" in message:
				sendMessage(s, db_get_points_user(user))

			### DEFAULT COMMANDS ###
			if "!localtime" in message:
				sendMessage(s, local_time())
			if "!admin" in message:
				sendMessage(s, basic_command('admin', user))
			if "!help" in message or "!commands" in message:
				sendMessage(s, basic_command('help', user))
			if "!twitter" in message:
				sendMessage(s, basic_command('twitter', user))
			if "!spooky" in message:
				sendMessage(s, basic_command('spooky', user))
			if "!bot" in message:
				sendMessage(s, basic_command('bot', user))
			if "!donger" in message:
				try:
					sendMessage(s, basic_command('donger', user))
				except:
					pass

			### UPDATE COMMANDS ###
			if "!coloring" in message:
				sendMessage(s, update_command('coloring', user))