import string
import re
import random
import datetime
import time

from Read import (getUser, getMessage, uptime, get_points, localtime, roulette, followage, raffle, mod_check, first, duel, check_points,
check_int )
from TheSocket import openSocket, sendMessage, sendWhisper
from Initialize import joinRoom
from Commands import commands
from temp import raffle_users
from Settings import ADMIN

s = openSocket()
joinRoom(s)
readbuffer = ""
temp_user = []
raffle_active = False
send_raffle_state = False
state = False

while True:
		readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)

			if "PING :tmi.twitch.tv" in line:
				#s.send(bytes(line.replace("PING", "PONG"), 'UTF-8'))
				response = "PONG :tmi.twitch.tv\r\n"
				print(response)
				#print(response)
				bytes_response = str.encode(response)
				#print(bytes_response)
				s.send(bytes_response)
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
			if "!followage" in message:
				sendMessage(s, followage(user))
			if "!first" in message:
				sendMessage(s, first())

			def time_up():
				time.sleep(15)
				sendMessage(s, "The raffle ends in 15 seconds!")
				time.sleep(15)
				time_up_time = datetime.datetime.now()
				return time_up_time

			# raffle
			raffle_amount = re.findall('\d+', message)
			y = str(raffle_amount)
			if ("!raffle") in message:
				if(mod_check(user)):
					enter_confirm = message.rsplit(" ")[2]
					# print(enter_confirm)
					new_y = int(re.search(r'\-?\d+', y).group())
					output = "Raffle for " + str(new_y) + " points has begun. Type " + enter_confirm + " to enter!"
					sendMessage(s, str(output))
					#startTime = datetime.datetime.now()
					raffle_active = True
					time_up()
					# print(raffle_users)
				else:
					sendMessage(s, "Only mods can set raffles FailFish")

			# collect raffle users
			if((raffle_active) and (str(enter_confirm) in message) and (user != ADMIN)):
				# print(user, " added to entrees")
				raffle_users.append(user)
				# print(raffle_users)
				sendMessage(s, raffle(new_y))

			# roulette
			amount = re.findall('\-?\d+', message)
			x = str(amount)
			# print("check this to see if int: ", x)
			# print(type(x))
			# print(x)
			if ("!roulette") in message:
				if(roulette(user, x) == False):
					roulette_error = user + ", you can only enter integer values."
					sendMessage(s, roulette_error)
					#sendWhisper(s, user, roulette_error)
				else:
					sendMessage(s, roulette(user, x))

			# duels
			if "!duel" in message:
				#state = True
				opponent = message.rsplit(" ")[1]
				temp_user.append(opponent)

				duel_amount = re.findall('\d+', message)
				# print(duel_amount[0])
				check_value = message.rsplit(" ")[2]

				if(check_int(check_value)):
					if(check_points(user, duel_amount[0])):
						output = opponent + ", " + user + " has challenged you to " + duel_amount[0] + " points. Type !accept to duel"
						sendMessage(s, output)
						state = True
					else:
						sendMessage(s, "Sorry, " + user + " you don't have enough points for that BabyRage")
				else:
					sendMessage(s, user + ", you can only enter integer values.")
			# print(temp_user)
			# print(user)
			if((state) and ("!accept" in message) and (user == temp_user[0])):
				state = False
				# print("duel accepted")
				sendMessage(s, duel(user, opponent, duel_amount[0]))
				temp_user.remove(opponent)
				# print(temp_user)


			# basic commands
			if "!admin" in message:
				sendMessage(s, commands.get('admin'))
			if "!commands" in message or "!help" in message:
				sendMessage(s, user + commands.get('commands'))
			if "!twitter" in message:
				sendMessage(s, commands.get('twitter'))
			if "!discord" in message:
				sendMessage(s, commands.get('discord'))
			if "!spooky" in message:
				sendMessage(s, commands.get('spooky'))
			if "!coloring" in message:
				sendMessage(s, commands.get('coloring'))