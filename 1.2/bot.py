import random
import re

from datetime import datetime, timedelta, date, time
from pytz import timezone

# external py files
from settings import twitch_irc
from basic_commands import commands, update_commands, friends
from sql import (db_add_user,
	db_add_points_user,
	db_minus_points_user,
	db_add_points_global,
	db_check_user,
	db_get_points_user,
	db_get_points_user_first,
	db_get_points_user_int)

wisp = "/me "

# get a user from the irc server
def get_user(line):

	seperate = line.split(":", 2)
	user = seperate[1].split("!", 1)[0]
	return user

# get a message sent in the irc server
def get_message(line):

	seperate = line.split(":", 2)
	message = seperate[2]
	return message

# get the local time of the streamer
def local_time():

	localtime = timezone('US/Eastern')
	time = datetime.now(localtime)
	format_time = time.strftime('%H:%M:%S')
	output = "{} Local time: {} EST".format(wisp, format_time)
	return output

def roulette(user, points):

	if(check_int(points)):
		int_points = get_int(points)
		if int_points <= 0:
			return(wisp + "{} you cannot gamble 0 or less points.".format(user))

		user_points = db_get_points_user_int(user)
		print(user_points)
		if int_points > user_points:
			return(wisp + "Sorry {}, you don't have enough points BabyRage".format(user))

		result = int_points * 2
		roll = random.randrange(1, 3)
		if(roll == 1):
			db_add_points_user(user, result)
			return(wisp + "{} won {} points! PogChamp".format(user, result))
		if(roll == 2):
			db_minus_points_user(user, result)
			return(wisp + "{} lost {} points! BibleThump".format(user, result))
	else:
		pass

def basic_command(key, user):

	if key == 'help':
		return wisp + user + commands.get('help')
	else:
		for keys, values in commands.items():
			if keys == key:
				return wisp + str(values)

def update_command(key, user):

	for keys, values in update_commands.items():
		if keys == key:
			return wisp + str(values)

def streamer(key):

	#print(key)
	return ''


### INT/STRING CHECKER FUNCTIONS ###

def word_n(string, n):

	output = string.split(" ")[n]
	return output

def get_int(string):

	output = int(re.search(r'\-?\d+', string).group())
	return output

def check_int(string):
	try:
		string = int(string)
		return True
	except(ValueError, TypeError):
		return False