import time
import re
from threading import Thread

# external py files
from modules.irc_socket import openSocket, sendMessage
from modules.irc_init import joinRoom
from bot import (get_user, get_message, local_time, basic_command, update_command,
	word_n, streamer_acorn, streamer_geek, roulette, check_int, get_int, uptime,
	followage, streamer, duel, quote, addquote, bttv_user_replace, raffle, 
	check_int_in_string, give_points, hug, latest_highlight, giveaway)
from modules.sql import (db_add_user,
	db_add_points_user,
	db_minus_points_user,
	db_add_points_global,
	db_check_user,
	db_get_points_user,
	db_get_points_user_first,
	db_get_points_user_int,
	db_get_user_rank,
	db_add_emote_count,
	db_get_emote_count,
	db_get_another_user_rank,
	db_add_counter1,
	db_get_counter1)
from modules.temp import (cooldown, temp_opponent, duel_state, temp_user, raffle_state,
	raffle_entries, raffle_amount, points_song_request, giveaway_entries, giveaway_state, 
	giveaway_time, giveaway_entry)
from modules.settings import twitch_irc
from modules.api import check_user_class, get_latest_follower, get_youtube_request, check_stream_online

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
					#time.sleep(440)
					time.sleep(120)
					print("[INFO] >>> Removed from cooldown array user: {}".format(cooldown[0]))
					cooldown.pop(0)
					print("[INFO] >>> Users in cooldown ", cooldown)

			def run():
					print("[INFO] >>> Cooldown timer started for roulette user: {}".format(user))
					rouletteTimer().start()

			class raffleTimer(Thread):
				def run(self):
					print("[INFO] >>> raffle timer started")
					time.sleep(30)
					sendMessage(s, "The raffle ends in 30 seconds!")
					time.sleep(30)
					global raffle_state
					raffle_state = False
					print("[DEBUG] >>> raffle state changed to {}".format(raffle_state))
					print("[DEBUG] >>> raffle timer stopped")
					sendMessage(s, raffle())
					# print("AFTER SENDING RAFFLE INFO >>> ", raffle_state)

			def raffle_run():
					raffleTimer().start()

			class giveawayTimer(Thread):
				def run(self):
					print("[INFO] >>> giveaway timer started!")
					global giveaway_time
					global giveaway_entry
					if giveaway_time == 1:
						half_time_sec = 30
					else:
						half_time = int(giveaway_time/2)
					half_time_sec = (half_time * 60)
					print("[INFO] >>> Half time[S]: ", half_time_sec)
					time.sleep(half_time_sec/2)
					sendMessage(s, "You have {} minutes left to enter the giveaway! Enter by typing {} in chat.".format(str(half_time), giveaway_entry))
					time.sleep(half_time_sec/2)
					global giveaway_state
					giveaway_state = False
					print("[DEBUG] >>> giveaway stated changed to {}".format(giveaway_state))
					print("[DEBUG] >>> giveaway timer stopped")
					sendMessage(s, giveaway())

			def giveaway_run():
					giveawayTimer().start()

			class duelTimer(Thread):
				def run(self):
					print("[INFO] >>> duel timer started")
					print(temp_opponent)
					print(temp_user)
					time.sleep(60)
					print("[INFO] >>> {} removed from duel queue")
					if(len(temp_opponent) == 0):
						print("[INFO] >>> No users to remove from duel cooldown")
					else:
						temp_opponent.pop(0)

			def duel_run():
					duelTimer().start()

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

			## ADMIN SUPER USER COMMANDS 
			if "!addpoints" in message and user == twitch_irc.get('CHANNEL'):
				add_points_user = char_2
				add_points_amount = char_3
				if(check_int(add_points_amount)):
					db_add_points_user(str(add_points_user), add_points_amount)
					sendMessage(s, "Admin gave {} points to {}.".format(add_points_amount, add_points_user))
			if "!minuspoints" in message and user == twitch_irc.get('CHANNEL'):
				min_points_user = char_2
				min_points_amount = char_3
				if(check_int(min_points_amount)):
					db_minus_points_user(str(min_points_user), min_points_amount)
					sendMessage(s, "Admin took {} points from {}.".format(min_points_amount, min_points_user))
			if "!shutdown" in message and user == twitch_irc.get('CHANNEL'):
				sendMessage(s, "Shutdown iniated by admin.. HeyGuys")
				raise SystemExit	

			#### POINT BASED COMMANDS ###

			# returns how many points a user owns
			if "!points" in message:
				db_add_user(user)
				sendMessage(s, db_get_points_user(user))

			# if "!givepoints" in message:
			# 	print(char_2)
			# 	print(char_3)
			# 	sendMessage(s, str(give_points(user, char_2, char_3)))

			if "!doggy" in message:
				sendMessage(s, "EleGiggle doggyfood has lost 1647359 points EleGiggle")

			if "!kritz" in message:
				sendMessage(s, "RAFFLE BabyRage KRITZWARE, RAFFLE BabyRage WE WANT RAFFLE KRITZ BabyRage")

			if "!fu" in message:
				try:
					test123 = char_2
					sendMessage(s, "Hey {} ( ° ͜ʖ͡°)╭∩╮".format(test123))
				except:
					pass

			if "!nice" in message:
				try:
					sendMessage(s, "☑ Stream online ☑ Earning points ☑ KappaPride in chat - Must be SKOWALZ stream FeelsGoodMan")
				except:
					pass

			if "!rank" in message:
				sendMessage(s, db_get_user_rank(user))
			# if "!userrank" in message:
			# 	rank_user_check = char_2
			# 	print(rank_user_check)
			# 	sendMessage(s, db_get_another_user_rank(rank_user_check))

			if "!roulette" in message and user not in cooldown:
				if(check_int(char_2)):
					sendMessage(s, roulette(user, char_2))
					cooldown.append(user)
					print("[INFO] >>> ", cooldown)
					run()
				else:
					sendMessage(s, "You can only enter int values {} BabyRage".format(user))

			if "!raffle" in message:
				#if(raffle_state == True):
				#	sendMessage(s, "A raffle is already active OpieOP")
				if(raffle_state == False):
					del raffle_entries[:]
					raffle_points = char_2
					if(check_user_class(user, "moderators")) and check_int(raffle_points):
						print("[DEBUG] >>> {} started a raffle for {} points".format(user, raffle_points))
						raffle_state = True
						raffle_amount.append(raffle_points)
						if(char_2[:1] == '-'):
							sendMessage(s, "A raffle has started for {} points! Type !join to enter Kappa".format(raffle_points))
						else:
							sendMessage(s, "A raffle has started for {} points! Type !join to enter PogChamp".format(raffle_points))
						raffle_run()
				else:
					sendMessage(s, "Raffle already active FailFish")


			if "!join" in message and raffle_state:
				raffle_entries.append(user)
				print("[DEBUG >>> Users in raffle entries >>> ", raffle_entries)
			if "!join" in message and raffle_state == False:
				sendMessage(s, "{}, there is currently no active raffle BabyRage".format(user))

			if "!giveaway" in message:
				if(giveaway_state == False):
					del giveaway_entries[:]
					giveaway_time = int(char_2)
					giveaway_entry = char_3
					if(check_user_class(user, "moderators")):
						print("[DEBUG] >>> {} started a giveaway!".format(user))
						giveaway_state = True
						sendMessage(s, "A giveaway has started. Type {} to enter! You have {} minutes..".format(giveaway_entry, giveaway_time))
						giveaway_run()
				else:
					sendMessage(s, "Giveaway already active FailFish")
			if giveaway_entry in message and giveaway_state == True:
				giveaway_entries.append(user)
				print("[DEBUG] >>> {} added to giveaway".format(user))
				print("[DEBUG] >>> Giveaway entries: {}".format(giveaway_entries))

			### DEBUG ###
			if "!test" in message:
				print(check_stream_online())



			if "!highlight" in message:
				sendMessage(s, latest_highlight())

			if "!songrequest" in message or "!requestsong" in message:
				if user == 'Moobot':
					print(error)
				else:
					try:
						char_2
						if(char_2):
							db_minus_points_user(user, points_song_request)
							sendMessage(s, "{} you just spent {} points on a song request! SeemsGood".format(user, points_song_request))
					except NameError:
						print("[ERROR] >>> No song request specified")

			#pogchamp count
			if "!emotecount" in message:
				emote = char_2
				sendMessage(s, str(db_get_emote_count(emote)))
			if "PogChamp" in message:
				db_add_emote_count("PogChamp")
			if "Kappa" in message:
				db_add_emote_count("Kappa")

			if "!duel" in message:
				test = re.match('(\w+\s\w+)', message[6:])
				if(test) == None:					
					sendMessage(s, "You didn't specify an amount {}! FailFish".format(user))
					break
				if(check_int(points_duel)):

					check_user_points = db_get_points_user_int(user)
					if(check_user_points < int(points_duel)):
						sendMessage(s, "Sorry {}, you don't have enough points for that BabyRage".format(user))
						break

					opponent = char_2
					format_opponent = bttv_user_replace(opponent)
					temp_opponent.append(opponent.lower())
					temp_user.append(user.lower())
					duel_state = True

					if(format_opponent == twitch_irc.get('NICK')):
						sendMessage(s, "{}, I always win the duel! MingLee".format(user))
						break

					duel_run()
					sendMessage(s, "{}, you have been challenged to {} points by {}! Type !accept to duel.".format(opponent, points_duel, user))
				else:
					sendMessage(s, "{} you can only enter integers! BabyRage".format(user))

					print(points_duel)
					print(temp_opponent)
					print(duel_state)

			if "!accept" in message and duel_state and (user in temp_user or user in temp_opponent):

				print("[DEBUG] >>> Points to duel >>> ", points_duel)
				print("[DEBUG] >>> Users in temp_opponent >>> {}".format(temp_opponent))
				try:
					# !duel pokchok 10
					user_to_duel = temp_opponent[0] # pokchok
					original_duel_user = temp_user[0] # kritzware
				except Exception as e:
					print(e)
					sendMessage(s, "{} you don't currently have an active duel Kappa".format(user))
					break

				print(user_to_duel)		
				print(original_duel_user) 	

				if(user in temp_opponent):
					print("[DEBUG] >>> Checking {} in temp_opponents".format(user))
					print(original_duel_user + " duelling " + user_to_duel)
					sendMessage(s, duel(original_duel_user, user_to_duel, points_duel))
					temp_opponent.remove(user_to_duel)
					temp_user.remove(original_duel_user)
					duel_state = False
					points_duel = ''
				else:
					print("[ERROR] >>> {} not found in temp_opponent".format(user))

			if "!hug" in message:
				try:
					sendMessage(s, hug(user, char_2))
				except:
					pass

			if "!+fucksgiven" in message:
				if(check_user_class(user, "moderators")):
					sendMessage(s, db_add_counter1(user))
			if "!fucksgiven" in message:
				sendMessage(s, db_get_counter1(user))
 

			# if "!songrequest" in message:
			# 	try:
			# 		char_2
			# 		sendMessage(s, get_youtube_request(user, char_2))
			# 	except NameError:
			# 		sendMessage(s, "no request")

			### ADVANCED COMMANDS ###
			if "!uptime" in message:
				print("[COMMAND] >>> !uptime")
				sendMessage(s, uptime())
			#if "!followage" in message:
			#	print("[COMMAND] >>> !followage")
			#	sendMessage(s, followage(user))
			if "!top" in message:
				print("[COMMAND] >>> !top")
				sendMessage(s, db_get_points_user_first()) 
			# if "!quote" in message:
			# 	print("[COMMAND] >>> !quote")
			# 	sendMessage(s, quote())
			# if "!addquote" in message:
			# 	print("[COMMAND] >>> !addquote")
			# 	sendMessage(s, addquote(quote_to_add))

			if "!followage" in message:
				print("[COMMAND] >>> !followage")
				sendMessage(s, followage(user))

			if "!streamer" in message:
				sendMessage(s, streamer(user, char_2))

			### DEFAULT COMMANDS ###
			if "!localtime" in message:
				print("[COMMAND] >>> !localtime")
				sendMessage(s, local_time('US/Eastern'))
			if "!gmt" in message:
				print("[COMMAND] >>> !gmt localtime")
				sendMessage(s, local_time('Europe/London'))
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
			if "!vampire" in message:
				sendMessage(s, basic_command('vampire', user))
			if "!bot" in message:
				print("[COMMAND] >>> !bot")
				sendMessage(s, basic_command('bot', user))
			if "!hype" in message:
				sendMessage(s, basic_command('hype', user))
			if "!chatlove" in message:
				sendMessage(s, basic_command('chatlove', user))
			if "!donger" in message:
				print("[COMMAND] >>> !donger")
				try:
					sendMessage(s, basic_command('donger', user))
				except:
					pass
			if "!wut" in message:
				# print("[COMMAND] >>> !wut")
				try:
					sendMessage(s, basic_command('wut', user))
				except:
					pass
			if "!rigged" in message:
				print("[COMMAND] >>> !rigged")
				sendMessage(s, basic_command('rigged', user))
			if "!raid" in message:
				print("[COMMAND] >>> !raid")
				sendMessage(s, basic_command('raid', user))

			if "!discord" in message:
				sendMessage(s, "Chat with other viewers on discord! discord.gg/0dlGiuDScFuAb2vx MingLee")

			# ### STREAMERS###
			# if "!streamer acorn" in message:
			# 	sendMessage(s, streamer_acorn(user))
			# if "!streamer geek" in message:
			# 	sendMessage(s, streamer_geek(user))

			### UPDATE COMMANDS ###
			if "!coloring" in message:
				print("[COMMAND] >>> !coloring")
				sendMessage(s, update_command('coloring', user))

			# if "!splinter" in message:
			# 	sendMessage(s, "NO FUN ALLOWED FUNgineer NO SONG REQUESTS FUNgineer")