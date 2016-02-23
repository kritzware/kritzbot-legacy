# external py files
from settings import twitch_irc

def get_user(line):

	seperate = line.split(":", 2)
	user = seperate[1].split("!", 1)[0]
	return user

def get_message(line):

	seperate = line.split(":", 2)
	message = seperate[2]
	return message