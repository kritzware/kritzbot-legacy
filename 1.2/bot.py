import random
import re
import string

from datetime import datetime, timedelta, date, time
from pytz import timezone

# external py files
from modules.settings import twitch_irc
from modules.basic_commands import commands, update_commands, friends
from modules.sql import (db_add_user,
	db_add_points_user,
	db_minus_points_user,
	db_add_points_global,
	db_check_user,
	db_get_points_user,
	db_get_points_user_first,
	db_get_points_user_int)
from modules.getjson import getJSON, getJSON_text

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

def uptime():

	data = getJSON('https://api.twitch.tv/kraken/channels/' + twitch_irc.get('CHANNEL') + '/videos?limit=1&broadcasts=true')
	latest_stream = data['videos'][0]['recorded_at']
	online = True

	timeformat = "%Y-%m-%dT%H:%M:%SZ"
	start_date = datetime.strptime(latest_stream, timeformat)
	current_date = datetime.utcnow()
	output_date = current_date - start_date - timedelta(microseconds=current_date.microsecond)

	online_check = getJSON('https://api.twitch.tv/kraken/streams/' + twitch_irc.get('CHANNEL'))
	if(online_check['stream'] == None):
		online = False

	hours = str(output_date)[:1]
	minutes = str(output_date)[2:4]

	if(online):
		return(wisp + "{} has been live for {} hrs, {} mins".format(twitch_irc.get('CHANNEL'), hours, minutes))
	else:
		return(wisp + "{} is not streaming at the moment FeelsBadMan".format(twitch_irc.get('CHANNEL')))


# get the local time of the streamer
def local_time():

	localtime = timezone('US/Eastern')
	time = datetime.now(localtime)
	format_time = time.strftime('%H:%M:%S')
	output = "{} Local time: {} EST".format(wisp, format_time)
	return output

def followage(user):

	try:
		data = getJSON_text("https://api.rtainc.co/twitch/followers/length?channel=" + twitch_irc.get('CHANNEL') + "&name=" + user)
		return(wisp + "{} has been following for {}! SeemsGood".format(user, data))
	except Exception as e:
		print("[ERROR] >>> ", e)
		return("{} is not following this channel! BibleThump".format(user))

def roulette(user, points):

	if(check_int(points)):
		int_points = get_int(points)
		if int_points <= 0:
			return(wisp + "{} you cannot gamble 0 or less points.".format(user))

		user_points = db_get_points_user_int(user)
		# print("[INFO] >>> User points: {}".format(user_points))
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

def streamer(user):

	acorn = "acorn"
	geek = "geek"

	if user.strip() == acorn.strip() or user.strip() == geek.strip():
		return ''
	else:
		output = wisp + "Check out {} at twitch.tv/{} VaultBoy".format(user, user)
		return output

def streamer_acorn():
	return wisp + friends.get('acorn')

def streamer_geek():
	return wisp + friends.get('geek')

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