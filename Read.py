import string
import json
import urllib.request

from datetime import datetime, timedelta, date, time
from Settings import CHANNEL
from TheSocket import openSocket, sendMessage

def getUser(line):

	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

def getMessage(line):

	separate = line.split(":", 2)
	message = separate[2]
	return message

def uptime():

	user = CHANNEL
	url = 'https://api.twitch.tv/kraken/channels/' + user + '/videos?limit=1&broadcasts=true'
	req = urllib.request.urlopen(url)
	data = json.loads(req.read().decode('UTF-8'))
	latestbroadcast = data['videos'][0]['recorded_at']
	online = True

	print("Broadcast start: " + latestbroadcast)

	#testing different time approach
	#url2 = 'https://api.twitch.tv/kraken/videos/' + latestbroadcast
	#req2 = urllib.request.urlopen(url2)
	#data2 = json.loads(req.read().decode('UTF-8'))
	#starttimestring = data2['recorded_at']

	timeformat = "%Y-%m-%dT%H:%M:%SZ"
	startdate = datetime.strptime(latestbroadcast, timeformat)
	currentdate = datetime.utcnow()
	combineddate = currentdate - startdate - timedelta(microseconds=currentdate.microsecond)

	check_request = urllib.request.urlopen('https://api.twitch.tv/kraken/streams/' + user)
	check_online = json.loads(check_request.read().decode('UTF-8'))
	if(check_online['stream'] == None):
		online = False

	hours = str(combineddate)[:1]
	minutes = str(combineddate)[2:4]

	if(online):
		print(combineddate)
		return(user + " has been live for " + hours + " hrs, " + minutes + " mins")
	else:
		return(user + " is not streaming at the moment FeelsBadMan")