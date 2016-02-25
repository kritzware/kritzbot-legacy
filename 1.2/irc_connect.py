import time
from threading import Thread

# external py files
from modules.irc_socket import openSocket, sendMessage
from modules.irc_init import joinRoom
from bot import (get_user,
	get_message,
	local_time,
	basic_command,
	update_command,
	word_n,
	streamer,
	roulette,
	check_int,
	get_int)
from modules.sql import (db_add_user,
	db_add_points_user,
	db_minus_points_user,
	db_add_points_global,
	db_check_user,
	db_get_points_user,
	db_get_points_user_first)
from modules.temp import cooldown
from modules.timers import cooldownTimer

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
			print("[MESSAGE] >>> " + user + " typed :" + message)

			### TIMER ###

			class cooldownTimer(Thread):

				def run(self):
					time.sleep(15)
					print("[INFO] >>> Removed from cooldown array user: {}".format(cooldown[0]))
					cooldown.pop(0)
					print("[INFO] >>> Users in cooldown ", cooldown)

			def run():
					print("[INFO] >>> Cooldown timer started for roulette user: {}".format(user))
					cooldownTimer().start()

			### STRING EXTRACTION ###
			try:
				char_2 = word_n(message, 1)
				only_int = get_int(message)
			except:
				pass

			#### POINT BASED COMMANDS ###

			# returns how many points a user owns
			if "!points" in message:
				sendMessage(s, db_get_points_user(user))
			if "!roulette" in message and user not in cooldown:
				sendMessage(s, roulette(user, char_2))
				cooldown.append(user)
				print("[INFO] >>> ", cooldown)
				run()

			### ADVANCED COMMANDS ###
			if "!streamer" in message:
				sendMessage(s, str(streamer(char_2)))

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