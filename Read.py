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
from temp import raffle_users

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

			result_points = ("/me " + check_user + " has " + format_points[0] + " points")

			if(int(format_points[0]) < 0):
				#print(int(format_points[0]))
				negative_checkpoints = ("/me " + check_user + " has -" + format_points[0] + " points BabyRage")
				return(str(negative_checkpoints))		

			return(str(result_points))
 
		if data[x] == str(check_user):

			check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
			return_points = check_db.fetchone()

			format_checkpoints = re.findall('[+-]?\d+(?:\.\d+)?', str(return_points))
			result_checkpoints = ("/me " + check_user + " has " + format_points[0] + " points")
			return(str(result_checkpoints))

	connection.close()

def check_user(user):

	check_db = connection.cursor()
	check_db.execute("SELECT user_id FROM table1")

	users = [row[0] for row in check_db.fetchall()]

	in_db = user in users

	if in_db:
		# print(user + " is in table")
		return(True)
	else:
		# print(user + " not in table: adding to db")
		check_db.execute("INSERT into table1 VALUES ( '" + user + "', " + str(0) + " )")
		return(True)

def bttv_quick_check(user):

	new_user = user.replace('@', '')
	return new_user

def check_points(user, points):

	check_db = connection.cursor()
	check_db.execute("SELECT points from table1 where user_id = '" + str(user) + "'")

	return_points = check_db.fetchone()
	format_points = re.findall('[+-]?\d+(?:\.\d+)?', str(return_points))

	try:
		format_points_int = int(format_points[0])
	except IndexError:
		format_points_int = 0

	# print(format_points)
	# print(format_points_int)
	# print(int(points))

	if(int(points) <= format_points_int):
		return True
	else:
		return False

def add_points():

	pointnum = 2 # 2 points per minute
	check_db = connection.cursor()
	check_db.execute("UPDATE table1 set points = points + " + str(pointnum))

def add_points_user(user, pointnum):

	check_db = connection.cursor()
	check_db.execute("UPDATE table1 set points = points + " + str(pointnum) + " where user_id = '" + str(user) + "' ")

def check_int(value):
	try:
		value = int(value)
		return True
	except ValueError:
		return False

def check_int_re(value):
	check_ints = re.findall('\d+', value)
	if not check_ints:
		# value is not an int
		return False
	else:
		# value is an int
		return True

def roulette(check_user, gamble):

	check_db = connection.cursor()

	if(check_int_re(gamble) == False):
		# return if user input is not an int
		roulette_true = False
		return(roulette_true)

	int_gamble = int(re.search(r'\-?\d+', gamble).group())

	# print("This is the int: ", int_gamble)

	if(int(int_gamble) <= 0):
		# print("test")
		return("/me " + check_user + " you cannot gamble 0 or less points.")

	# check if user has enough points to gamble
	check_db.execute("SELECT points from table1 where user_id = '" + check_user + "'")
	return_points = check_db.fetchone()
	format_checkpoints = re.findall('[+-]?\d+(?:\.\d+)?', str(return_points))
	# print(format_checkpoints[0])
	# print(int(format_checkpoints[0]))

	if(int(int_gamble) > int(format_checkpoints[0])):
		return("/me " + "Sorry " + check_user + ", you don't have enough points for that BabyRage")

	result = int_gamble * 2
	# print(result)

	roll = random.randrange(1, 3)
	if(roll == 1):
		check_db.execute("UPDATE table1 set points = points + " + str(result) + " where user_id = '" + str(check_user) + "' ")
		#return(check_user + " gambled " + str(int_gamble) + " points and won " + str(result) + " points! PogChamp")
		return("/me " + check_user + " won " + str(result) + " points! PogChamp")
	if(roll == 2):
		check_db.execute("UPDATE table1 set points = points - " + str(int_gamble) + " WHERE user_id = '" + str(check_user) + "' ")
		#return(check_user + " gambled " + str(int_gamble) + " points and lost " + str(result) + " points! BibleThump")
		return("/me " + check_user + " lost " + str(int_gamble) + " points! BibleThump")

 
def followage(follower):

	url = "https://api.rtainc.co/twitch/followers/length?channel=" + CHANNEL + "&name=" + str(follower)
	get_age = urllib.request.urlopen(url)
	output = get_age.read()
	output_string = output.decode('UTF-8')
	return("/me " + str(follower) + " has been following for " + output_string + "! SeemsGood")

def first():

	check_db = connection.cursor()
	check_db.execute("SELECT MAX(points) FROM table1")
	first_points = check_db.fetchone()
	# print(first_points)
	format_first_points = re.findall('[+-]?\d+(?:\.\d+)?', str(first_points))
	# print(format_first_points)

	check_db.execute("SELECT user_id from table1 WHERE points = " + format_first_points[0])
	first_user = check_db.fetchone()
	# print(first_user)

	output = str("/me " + first_user[0]) + " has the most points: " + str(format_first_points[0])
	return(output)

def duel(user, opponent, points):

	check_db = connection.cursor()

	win = int(points)

	if(api_request_chatters_check(opponent, "viewers") or api_request_chatters_check(opponent, "moderators")):
		if(check_user(user) and check_user(opponent)):
			roll = random.randrange(1, 3)
			if(roll == 1):
				print(user)
				check_db.execute("UPDATE table1 set points = points + " + str(points) + " WHERE user_id = '" + str(user) + "' ")
				check_db.execute("UPDATE table1 set points = points - " + str(points) + " WHERE user_id = '" + str(opponent) + "' ")
				return("/me " + user + " won the duel! They get " + str(win) + " points PogChamp")
			if(roll == 2):
				print(opponent)
				check_db.execute("UPDATE table1 set points = points + " + str(points) + " WHERE user_id = '" + str(opponent) + "' ")
				check_db.execute("UPDATE table1 set points = points - " + str(points) + " WHERE user_id = '" + str(user) + "' ")
				return("/me " + opponent + " won the duel! They get " + str(win) + " points PogChamp")
		else:
			return("/me " + "Fatal error occured WutFace")
	else:
		return("/me " + "Error: User not found WutFace")


def raffle(draw):

	raffle_users_sorted = list(set(raffle_users))
	print(raffle_users_sorted)
	winner = random.choice(raffle_users_sorted)
	
	add_points_user(winner, draw)
	return("/me " + "The winner is " + winner + " !! PogChamp")	

def api_request_chatters_check(user, user_class):

	user_class_str = str(user_class)
	url = 'https://tmi.twitch.tv/group/user/' + CHANNEL + '/chatters'
	# print(url)
	try:
		req = urllib.request.urlopen(url)
		data = json.loads(req.read().decode('UTF-8'))
		chatters = data['chatters'][user_class_str]
		for n in chatters:
			if(n == user):
				print("user found in class", user_class)
				return(True)
			else:
				return(False)
	except urllib.error.URLError as e:
		print("API error:")
		print(e.reason)
		return("/me " + "Error: Twitch API down BabyRage")

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
		return("/me " + user_channel + " has been live for " + hours + " hrs, " + minutes + " mins")
	else:
		return("/me " + user_channel + " is not streaming at the moment FeelsBadMan")

def localtime():

	local_time = timezone('US/Eastern')
	time = datetime.now(local_time)
	time_format = time.strftime('%H:%M:%S')
	time_format_str = "/me " + "Local time: " + str(time_format) + " EST"
	return(time_format_str)