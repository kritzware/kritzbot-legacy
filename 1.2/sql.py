import pymysql

# external py files
from settings import db_host, db_user, db_pass, db_name, db_autocommit

connection = pymysql.connect(
	host = db_host,
	user = db_user,
	password = db_pass,
	db = db_name,
	autocommit = db_autocommit)
 
 # connect to the database
def db_connect():

	pybot = connection.cursor()
	return pybot

# close connection to the database
def db_close():

	return connection.close()

# add user to the database
def db_add_user(user):

	db_connect()
	pybot.execute("INSERT ignore into table1 VALUES ('" + str(user) + "', " + str(0) + " )")
	db_close()

# add points to a user in the database
def db_add_points_user(user, points):

	db_connect()
	pybot.execute("UPDATE table1 set points = points + " + str(points) + " where user_id = '" + str(user) + "' ")

# add points to all users in the database
def db_add_points_global(points):

	db_connect()
	pybot.execute("UPDATE table1 set points = points + " + str(points))
	db_close()

# get points of a user in the database
def db_get_points_user(user):

	db_connect()
	count = pybot.execute("SELECT COUNT(*) FROM table1")
	pybot.execute("SELECT user_id from table1")
	users = pybot.fetchall()

	for n in range(0, count + 1):

		if data[n] != str(user):
			db_add_points_user(user)
			pybot.execute("SELECT points from table1 where user_id = '" + user + "'")
			
			get_points = pybot.fetchone()
			format_points = db_format(get_points)
			output = ("/me " + user + " has " + format_points + " points")

			if(int(format_points) < 0):
				negative_output = ("/me " + user + " has -" + format_points + " points BabyRage")
				return str(negative_output)
			else:
				return output

		if data[n] == str(user):
			pybot.execute("SELECT points from table1 where user_id = '" + user + "'")

			get_points = pybot.fetchone()
			format_points = db_format(get_points)
			output = ("/me " + user + " has " + format_points + " points")
			return output
	db_close()

# format parameter value to get first int result
def db_format(values):

	format_values = re.findall('[+-]?\d+(?:\.\d+)?', str(values))
	return format_values[0]