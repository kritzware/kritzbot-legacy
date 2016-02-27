import json
import urllib.request

from datetime import datetime, timedelta, date, time
from modules.settings import twitch_irc

latest_follower = ''

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
		chatters = data['chatters'][user_class]

		print("[DEBUG] >>> " + str(user_class) + " IN CHAT >>> ", chatters)

		for n in chatters:
			
			print("[DEBUG] >>> CHECKING >>> ", n)

			if(n == user):
				print("[INFO] >>> " + user + " found in class " + user_class)
				return(True)

	except urllib.error.URLError as e:
		print("[ERROR] >>> ", e.reason)
		return("Error: Twitch API down BabyRage")

def get_latest_follower():

	data = getJSON("https://api.twitch.tv/kraken/channels/" + twitch_irc.get('CHANNEL') + "/follows/?limit=1")
	follower = data["follows"][0]['user']['name']
	print("[INFO] >>> Latest follower >>> ", follower)
	latest_follower = "test_follower"

	check_new_follower = get_latest_follower()
	if(latest_follower != check_new_follower):
		return("Thanks for following {} HeyGuys".format(latest_follower))
	else:
		return("")