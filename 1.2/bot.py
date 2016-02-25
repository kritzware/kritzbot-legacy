from datetime import datetime, timedelta, date, time
from pytz import timezone

# external py files
from settings import twitch_irc
from basic_commands import commands, update_commands

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