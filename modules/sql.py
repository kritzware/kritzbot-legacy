import pymysql
import re

# external py files
from modules.settings import db_host, db_user, db_pass, db_name, db_autocommit

connection = pymysql.connect(
	host = db_host,
	user = db_user,
	password = db_pass,
	db = db_name,
	autocommit = db_autocommit)

pybot = connection.cursor()

# close connection to the database
def db_close():

	return connection.close()

# add user to the database
def db_add_user(user):

	pybot.execute("INSERT ignore into table1 VALUES ('" + str(user) + "', " + str(0) + " )")

# add points to a user in the database
def db_add_points_user(user, points):

	pybot.execute("UPDATE table1 set points = points + " + str(points) + " where user_id = '" + str(user) + "' ")

# increments 1 to emote count value
def db_add_emote_count(emote):

	pybot.execute("UPDATE emote_table set count = count + 1 where emote = '" + str(emote) + "' ")

# gets the emote count for certain emote
def db_get_emote_count(emote):

	count = pybot.execute("SELECT COUNT(*) FROM emote_table")
	pybot.execute("SELECT emote from emote_table")
	emotes = pybot.fetchall()

	emote_range = len(emotes)
	pogchamp = ''.join(emotes[0])

	pybot.execute("SELECT count from emote_table where emote = '" + str(pogchamp) + "'")
	get_count = pybot.fetchone()
	format_count = db_format(get_count)
	output = "{} has been used {} times in the chat! {}".format(pogchamp, format_count, pogchamp)
	return str(output)

# add points to all users in the database
def db_add_points_global(points):

	pybot.execute("UPDATE table1 set points = points + " + str(points))

def db_minus_points_user(user, points):

	pybot.execute("UPDATE table1 set points = points - " + str(points) + " where user_id = '" + str(user) + "' ")

# get points of a user in the database
def db_get_points_user(user):

	count = pybot.execute("SELECT COUNT(*) FROM table1")
	pybot.execute("SELECT user_id from table1")
	users = pybot.fetchall()

	for n in range(0, count + 1):

		if users[n] != str(user):
			db_add_points_user(user, 0)
			pybot.execute("SELECT points from table1 where user_id = '" + str(user) + "'")
			
			get_points = pybot.fetchone()
			format_points = db_format(get_points)
			output = ("/me " + user + " has " + format_points + " points")

			if(int(format_points) < 0):
				negative_output = ("/me " + user + " has -" + format_points + " points BabyRage")
				return str(negative_output)
			else:
				return output

		if users[n] == str(user):
			pybot.execute("SELECT points from table1 where user_id = '" + user + "'")

			get_points = pybot.fetchone()
			format_points = db_format(get_points)
			output = ("/me " + user + " has " + format_points + " points")
			return output

def db_get_points_user_int(user):

	points = pybot.execute("SELECT points from table1 where user_id = '" + str(user) + "'")
	get_points = pybot.fetchone()
	return int(db_format(get_points))

def db_check_user(user):

	pybot.execute("SELECT user_id FROM table1")

	users = [row[0] for row in pybot.fetchall()]
	in_db = user in users

	if in_db:
		return True
	else:
		db_add_user(user)
		db_add_points_user(user, 0)
		return True

def db_get_points_user_first():

	pybot.execute("SELECT MAX(points) FROM table1")
	most_points = pybot.fetchone()
	format_most_points = db_format(str(most_points))
	pybot.execute("SELECT user_id from table1 WHERE points = " + format_most_points)
	most_user = pybot.fetchone()
	output = str("/me " + most_user[0] + " has the most points: " + str(format_most_points) + " PogChamp")
	return(output)

def db_get_user_total():

	pybot.execute("SELECT COUNT(*) AS user_id FROM table1")
	user_total = pybot.fetchone()
	format_user_total = db_format(str(user_total))
	return(str(format_user_total))

def db_get_user_rank(user):

	try:
		pybot.execute("SELECT 1 + (SELECT count(*) FROM table1 a WHERE a.points > b.points ) AS rank FROM table1 b WHERE user_id = '" + str(user) + "' ORDER BY rank LIMIT 1")
		ranking = pybot.fetchone()
		format_ranking = db_format(ranking)
		format_points = db_get_points_user_int(user)
		total_users = db_get_user_total()
		output = "You are rank {} out of {} {}, with {} points!".format(str(format_ranking), total_users, user, format_points)
		return output
	except Exception:
		db_add_user(user)
		return "You are at the bottom {}, with {} points FeelsBadMan".format(user, db_get_points_user_int(user))

def db_get_another_user_rank(user):

	pybot.execute("SELECT 1 + (SELECT count(*) FROM table1 a WHERE a.points > b.points ) AS rank FROM table1 b WHERE user_id = '" + str(user) + "' ORDER BY rank LIMIT 1")
	ranking = pybot.fetchone()
	print(ranking)
	format_ranking = db_format(ranking)
	print(format_ranking)
	format_points = db_get_points_user(user)
	print(format_points)
	total_users = db_get_user_total()
	output = "{} is rank {} out of {}, with {} points!".format(user, str(format_ranking), total_users, format_points)
	return output
	
# format parameter value to get first int result
def db_format(values):

	format_values = re.findall('[+-]?\d+(?:\.\d+)?', str(values))
	return format_values[0]