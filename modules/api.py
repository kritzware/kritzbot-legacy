import json
import urllib.request

from datetime import datetime, timedelta, date, time
from modules.settings import twitch_irc

def getJSON(url):

	request = urllib.request.urlopen(url)
	data = json.loads(request.read().decode('UTF-8'))
	return data

def getJSON_text(url):

	request = urllib.request.urlopen(url)
	data = request.read()
	data_string = data.decode('UTF-8')
	return data_string

def check_user_class(user, user_class):

	try:
		data = getJSON('https://tmi.twitch.tv/group/user/' + twitch_irc.get('CHANNEL') + '/chatters')
		chatters = data['chatters'][str(user_class)]

		for n in chatters:

			print(n)
			print(str(user))

			if(n == str(user)):
				print("[INFO] >>> " + user + " found in class " + user_class)
				return(True)
			else:
				return(False)
	except urllib.error.URLError as e:
		print("[ERROR] >>> ", e.reason)
		return("Error: Twitch API down BabyRage")