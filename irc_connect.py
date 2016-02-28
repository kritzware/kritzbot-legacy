import time
import re
from threading import Thread

# external py files
from modules.irc_socket import openSocket, sendMessage
from modules.irc_init import joinRoom
from bot import (get_user, get_message, local_time, basic_command, update_command,
	word_n, streamer_acorn, streamer_geek, roulette, check_int, get_int, uptime,
	followage, streamer, duel, quote, addquote, bttv_user_replace, raffle)
from modules.sql import (db_add_user,
	db_add_points_user,
	db_minus_points_user,
	db_add_points_global,
	db_check_user,
	db_get_points_user,
	db_get_points_user_first)
from modules.temp import (cooldown, temp_opponent, duel_state, temp_user, 
	raffle_state, raffle_entries, raffle_amount)
from modules.settings import twitch_irc
from modules.api import check_user_class, get_latest_follower

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

			class raffleTimer(Thread):

				def run(self):
					print("raffle timer started")
					time.sleep(30)
					sendMessage(s, "The raffle ends in 30 seconds!")
					time.sleep(30)
					raffle_state = False
					print("[DEBUG] >>> raffle timer stopped")
					sendMessage(s, raffle())

			def raffle_run():
					raffleTimer().start()

			### STRING EXTRACTION ###
			try:
				char_1 = word_n(message, 0)
				char_2 = word_n(message, 1)
				char_3 = word_n(message, 2)
				points_duel = char_3
				quote_to_add = message[10:]
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

			if "!raffle" in message:
				raffle_points = char_2
				if(check_user_class(user, "moderators")) and check_int(raffle_points):
					print("[DEBUG] >>> {} started a raffle for {} points".format(user, raffle_points))
					raffle_state = True
					raffle_amount.append(raffle_points)
					sendMessage(s, "A raffle has started for {} points! Type !join to enter PogChamp".format(raffle_points))
					raffle_run()

			if "!join" in message and raffle_state:
				raffle_entries.append(user)
			if "!join" in message and raffle_state == False:
				sendMessage(s, "{}, there is currently no active raffle BabyRage".format(user))

			if "!test" in message:
				print(raffle_entries)


			if "!duel" in message:
				#test = re.match('(\w+\s\w+)', char_2[:-1])
				#if(test) == None:					
				#	sendMessage(s, "You didn't specify an amount {}! FailFish".format(user))
				#	break
				if(check_int(char_3)):
					opponent = char_2
					format_opponent = bttv_user_replace(opponent)
					temp_opponent.append(opponent.lower())
					temp_user.append(user.lower())
					duel_state = True

					if(format_opponent == twitch_irc.get('NICK')):
						sendMessage(s, "{}, I always win the duel! MingLee".format(user))
						break

					sendMessage(s, "{}, you have been challenged to {} points by {}! Type !accept to duel.".format(opponent, points_duel, user))
				else:
					sendMessage(s, "{} you can only enter integers! BabyRage".format(user))

					print(points_duel)
					print(temp_opponent)
					print(duel_state)

			if "!accept" in message and duel_state:

				print("[DEBUG] >>> Points to duel >>> ", points_duel)
				print("[DEBUG] >>> Users in temp_opponent >>> {}".format(temp_opponent))
				try:
					user_to_duel = temp_opponent[0]
					original_duel_user = temp_user[0]
				except Exception as e:
					print(e)
					sendMessage(s, "{} you don't currently have an active duel Kappa".format(user))
					break

				print(user_to_duel)
				print(original_duel_user)

				if(user == user_to_duel):
					print("[DEBUG] >>> Checking {} in temp_opponents".format(user))
					print(original_duel_user + " duelling " + user_to_duel)
					sendMessage(s, duel(original_duel_user, user_to_duel, points_duel))
					print(type(user_to_duel))
					temp_opponent.remove(user_to_duel)
					temp_user.remove(original_duel_user)
				else:
					print("[ERROR] >>> {} not found in temp_opponent".format(temp_opponent[0]))


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
			if "!quote" in message:
				print("[COMMAND] >>> !quote")
				sendMessage(s, quote())
			if "!addquote" in message:
				print("[COMMAND] >>> !addquote")
				sendMessage(s, addquote(quote_to_add))

			if "!followage" in message:
				print("[COMMAND] >>> !followage")
				sendMessage(s, followage(user))

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