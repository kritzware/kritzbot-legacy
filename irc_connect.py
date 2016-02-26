import time
from threading import Thread

# external py files
from modules.irc_socket import openSocket, sendMessage
from modules.irc_init import joinRoom
from bot import (get_user, get_message, local_time, basic_command, update_command,
	word_n, streamer_acorn, streamer_geek, roulette, check_int, get_int, uptime,
	followage, streamer)
from modules.sql import (db_add_user,
	db_add_points_user,
	db_minus_points_user,
	db_add_points_global,
	db_check_user,
	db_get_points_user,
	db_get_points_user_first)
from modules.temp import cooldown

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
				print("[IRC] >>> ", response)
				bytes_response = str.encode(response)
				s.send(bytes_response)
				break
			user = get_user(line)
			message = get_message(line)
			print("[MESSAGE] >>> " + user + " typed :" + message)

			### TIMER ###

			class rouletteTimer(Thread):

				def run(self):
					time.sleep(440)
					print("[INFO] >>> Removed from cooldown array user: {}".format(cooldown[0]))
					cooldown.pop(0)
					print("[INFO] >>> Users in cooldown ", cooldown)

			def run():
					print("[INFO] >>> Cooldown timer started for roulette user: {}".format(user))
					rouletteTimer().start()

			### STRING EXTRACTION ###
			try:
				char_1 = word_n(message, 0)
				char_2 = word_n(message, 1)
				only_int = get_int(message)
			except:
				pass

			#### POINT BASED COMMANDS ###

			# returns how many points a user owns
			if "!points" in message:
				sendMessage(s, db_get_points_user(user))
			if "!roulette" in message and user not in cooldown:
				if(check_int(char_2)):
					sendMessage(s, roulette(user, char_2))
					cooldown.append(user)
					print("[INFO] >>> ", cooldown)
					run()
				else:
					sendMessage(s, "You can only enter int values {} BabyRage".format(user))

			### ADVANCED COMMANDS ###
			if "!uptime" in message:
				print("[COMMAND] >>> !uptime")
				sendMessage(s, uptime())
			if "!followage" in message:
				print("[COMMAND] >>> !followage")
				sendMessage(s, followage(user))
			if "!top" in message:
				print("[COMMAND] >>> !top")
				sendMessage(s, db_get_points_user_first()) 
			if "!followage" in message:
				print("[COMMAND] >>> !followage")
				sendMessage(s, followage(user))
				break

			if "!streamer" in message:
				sendMessage(s, streamer(user, char_2))

			### DEFAULT COMMANDS ###
			if "!localtime" in message:
				print("[COMMAND] >>> !localtime")
				sendMessage(s, local_time())
			if "!admin" in message:
				print("[COMMAND] >>> !admin")
				sendMessage(s, basic_command('admin', user))
			if "!help" in message or "!commands" in message:
				print("[COMMAND] >>> !help")
				sendMessage(s, basic_command('help', user))
			if "!twitter" in message:
				print("[COMMAND] >>> !twitter")
				sendMessage(s, basic_command('twitter', user))
			if "!spooky" in message:
				print("[COMMAND] >>> !spooky")
				sendMessage(s, basic_command('spooky', user))
			if "!bot" in message:
				print("[COMMAND] >>> !bot")
				sendMessage(s, basic_command('bot', user))
			if "!donger" in message:
				print("[COMMAND] >>> !donger")
				try:
					sendMessage(s, basic_command('donger', user))
				except:
					pass

			# ### STREAMERS###
			# if "!streamer acorn" in message:
			# 	sendMessage(s, streamer_acorn(user))
			# if "!streamer geek" in message:
			# 	sendMessage(s, streamer_geek(user))

			### UPDATE COMMANDS ###
			if "!coloring" in message:
				print("[COMMAND] >>> !coloring")
				sendMessage(s, update_command('coloring', user))