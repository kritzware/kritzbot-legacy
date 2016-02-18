import string
import json
import urllib.request
import requests
import pymysql
import re

from datetime import datetime, timedelta, date, time
from Settings import CHANNEL, connection
from TheSocket import openSocket, sendMessage

def getUser(line):

	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

def getMessage(line):

	separate = line.split(":", 2)
	message = separate[2]
	return message

def get_points(check_user):

	check_db = connection.cursor()
	check_db.execute("SELECT user_id from table1")

	data = check_db.fetchall()

	check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
	points = check_db.fetchall()
	
	strpoints = str(points)
	formatp = re.findall('\d+', strpoints)

	result = (check_user + " has " + formatp[0] + " points")
	return(result)

	# result = check_user + " has {} " + " points".format(points[0:3])
	# print(result)
	# return(str(result))

	# if check_user in check_db.fetchall():
	# 	points = check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
	# 	print("user points found")
	# 	return check_user + " has" + points + " points"
	# else:
	# 	check_db.execute("INSERT INTO table1 VALUES ( '" + check_user + "', " + str(0) + " )")
	# 	print("adding new user to db")
	# 	return check_user + " has 0 points FeelsBadMan"
 
	connection.close()


def uptime():

	user_channel = CHANNEL
	url = 'https://api.twitch.tv/kraken/channels/' + user_channel + '/videos?limit=1&broadcasts=true'
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

	check_request = urllib.request.urlopen('https://api.twitch.tv/kraken/streams/' + user_channel)
	check_online = json.loads(check_request.read().decode('UTF-8'))
	if(check_online['stream'] == None):
		online = False

	hours = str(combineddate)[:1]
	minutes = str(combineddate)[2:4]

	if(online):
		print(combineddate)
		return(user_channel + " has been live for " + hours + " hrs, " + minutes + " mins")
	else:
		return(user_channel + " is not streaming at the moment FeelsBadMan")