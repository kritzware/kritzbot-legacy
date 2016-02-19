import string
import json
import urllib.request
import requests
import pymysql
import re
import random

from pytz import timezone
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
	count = check_db.execute("SELECT COUNT(*) FROM table1")
	#print(count) # prints no. of rows
	check_db.execute("SELECT user_id from table1")
	data = check_db.fetchall() 
	#print(data) # print user_id rows

	for x in range(0, count + 1):

		if data[x] != str(check_user):

			check_db.execute("INSERT ignore into table1 VALUES ( '" + check_user + "', " + str(0) + " )")
			check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
			points = check_db.fetchone()
			#print(points)

			format_points = re.findall('[+-]?\d+(?:\.\d+)?', str(points))
			#print(format_points)

			result_points = (check_user + " has " + format_points[0] + " points")

			if(int(format_points[0]) < 0):
				#print(int(format_points[0]))
				negative_checkpoints = (check_user + " has -" + format_points[0] + " points BabyRage")
				return(str(negative_checkpoints))		

			return(str(result_points))
 
		if data[x] == str(check_user):

			check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
			return_points = check_db.fetchone()

			format_checkpoints = re.findall('[+-]?\d+(?:\.\d+)?', str(return_points))
			result_checkpoints = (check_user + " has " + format_points[0] + " points")
			return(str(result_checkpoints))

	connection.close()

def add_points():

	pointnum = 16 # 4 points per minute
	check_db = connection.cursor()
	check_db.execute("UPDATE table1 set points = points + " + str(pointnum))

def roulette(check_user, gamble):

	check_db = connection.cursor()

	int_gamble = int(re.search(r'\-?\d+', gamble).group())

	print(int_gamble)

	if(int(int_gamble) <= 0):
		#print("test")
		return(check_user + " you cannot gamble 0 or less points.")

	# check if user has enough points to gamble
	check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
	return_points = check_db.fetchone()
	format_checkpoints = re.findall('[+-]?\d+(?:\.\d+)?', str(return_points))
	#print(format_checkpoints[0])
	#print(int(format_checkpoints[0]))

	if(int(int_gamble) > int(format_checkpoints[0])):
		return("Sorry " + check_user + ", you don't have enough points.")

	result = int_gamble * 2
	#print(result)

	roll = random.randrange(1, 3)
	if(roll == 1):
		check_db.execute("UPDATE table1 set points = points + " + str(result) + " where user_id = '" + str(check_user) + "' ")
		#return(check_user + " gambled " + str(int_gamble) + " points and won " + str(result) + " points! PogChamp")
		return(check_user + " won " + str(result) + " points! PogChamp")
	if(roll == 2):
		check_db.execute("UPDATE table1 set points = points - " + str(int_gamble) + " WHERE user_id = '" + str(check_user) + "' ")
		#return(check_user + " gambled " + str(int_gamble) + " points and lost " + str(result) + " points! BibleThump")
		return(check_user + " lost " + str(int_gamble) + " points! BibleThump")

	#ADD POINTS
	#UPDATE table1 set points = points + 10 where user_id = 'kritzware';


	# for x in data:
	# 	if check_user not in data:
	# 		print("user not found, adding to database")
	# 		check_db.execute("INSERT into table1 VALUES ( '" + check_user + "', " + str(0) + " )")
	# 		check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
			
	# 		new_points = check_db.fetchone()
	# 		strnew_points = str(new_points)

	# 		format_newpoints = re.findall('\d+', strnew_points)
	# 		new_result = (check_user + " has " + format_newpoints[0] + " points")
	# 		return(strnew_points)

	# else:
	# 	check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")

	# 	points = check_db.fetchall()
	# 	strpoints = str(points)
	
	# 	formatp = re.findall('\d+', strpoints)
	# 	result = (check_user + " has " + formatp[0] + " points")
	# 	return(result)

	# result = check_user + " has {} " + " points".format(points[0:3])
	# print(result)
	# return(str(result))

	# if check_user in check_db.fetchall():
	# 	points = check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
	# 	print("user points found")
	# 	return check_user + " has" + points + " points"
	# else:
	# 	check_db.execute("INSERT into table1 VALUES ( '" + check_user + "', " + str(0) + " )")
	# 	print("adding new user to db")
	# 	return check_user + " has 0 points FeelsBadMan"
 
	


def uptime():

	user_channel = CHANNEL
	url = 'https://api.twitch.tv/kraken/channels/' + user_channel + '/videos?limit=1&broadcasts=true'
	req = urllib.request.urlopen(url)
	data = json.loads(req.read().decode('UTF-8'))
	latestbroadcast = data['videos'][0]['recorded_at']
	online = True

	#print("Broadcast start: " + latestbroadcast)

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
		#print(combineddate)
		return(user_channel + " has been live for " + hours + " hrs, " + minutes + " mins")
	else:
		return(user_channel + " is not streaming at the moment FeelsBadMan")

def localtime():

	local_time = timezone('US/Eastern')
	time = datetime.now(local_time)
	time_format = time.strftime('%H:%M:%S')
	time_format_str = "Local time: " + str(time_format) + " EST"
	return(time_format_str)