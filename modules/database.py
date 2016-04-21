import pymysql
import re
import logging, coloredlogs
from modules.config import *

class Database:

	def __init__(self, host, user, password, name, autocommit):
		self.host = host
		self.user = user
		self.password = password
		self.name = name
		self.autocommit = autocommit
		self.db = self.database_connection()

	def database_connection(self):
		logging.info("Connecting to database..")
		connection = pymysql.connect(
			host = self.host,
			user = self.user,
			password = self.password,
			db = self.name,
			autocommit = self.autocommit
		)
		db = connection.cursor()
		return db

	def db_format(self, data):
		format_data = re.findall('[+-]?\d+(?:\.\d+)?', str(data))
		return format_data[0]

	def db_tuple_to_string(self, data):
		return ''.join(data)

	def db_add_user(self, user):
		self.db.execute("INSERT ignore into table1 VALUES ('{}', 0)".format(user))

	def db_add_points_user(self, user, points):
		self.db.execute("UPDATE table1 set points = points + {} where user_id = '{}'".format(points, user))

	def db_minus_points_user(self, user, points):
		self.db.execute("UPDATE table1 set points = points - {} where user_id = '{}'".format(points, user))

	def db_check_user_exists(self, user):
		points = self.db.execute("SELECT user_id FROM table1 where user_id = '{}'".format(user))
		check_user_exists = self.db.fetchone()
		if(check_user_exists == None):
			return False
		else:
			return True

	def bttv_parse(self, username):
		output = username.replace('@', '')
		return output

	def db_get_points_user(self, user, self_user):
		user = self.bttv_parse(user)
		points = self.db_get_user_points_int(user)

		if(points < 0):
			output = "{}, you have {} {} BabyRage".format(user, points, CURRENCY)
		else:
			output = "{}, you have {} {}".format(user, points, CURRENCY)
			print(user)
			print(self.user)
			if(user != self_user):
				output = "{} has {} {}".format(user, points, CURRENCY)
		return output

	def db_get_user_points_int(self, user):
		points = self.db.execute("SELECT points from table1 where user_id = '{}'".format(user))
		get_points = self.db.fetchone()
		#if(get_points == None):
		#	self.db_add_user(user)
		#	points = self.db.execute("SELECT points from table1 where user_id = '{}'".format(user))
		#	get_points = self.db.fetchone()
		return int(self.db_format(get_points))

	def db_get_user_total(self):
		self.db.execute("SELECT COUNT(*) AS user_id FROM table1")
		user_total = self.db.fetchone()
		format_user_total = self.db_format(str(user_total))
		return(str(format_user_total))

	def db_get_user_rank(self, user):
		user = self.bttv_parse(user)
		#try:
		self.db.execute("SELECT 1 + (SELECT count(*) FROM table1 a WHERE a.points > b.points ) AS rank FROM table1 b WHERE user_id = '{}' ORDER BY rank LIMIT 1".format(user))
		ranking = self.db.fetchone()
		format_ranking = self.db_format(ranking)
		format_points = self.db_get_user_points_int(user)
		total_users = self.db_get_user_total()
		output = "{} is rank {} out of {}, with {} {}!".format(user, str(format_ranking), total_users, format_points, CURRENCY)
		return output
		#except Exception:
		#	self.db_add_user(user)
		#	points = self.db_get_user_points_int(user)
		#	return "{} is the lowest rank, with {} {} FeelsBadMan".format(user, points, CURRENCY)

	def db_get_follower(self):
		self.db.execute("SELECT follower FROM latest_follower")
		follower = self.db.fetchall()
		follower_parsed = self.db_tuple_to_string(follower[0])
		return follower_parsed

	def db_new_follower(self, follower):
		self.db.execute("UPDATE latest_follower SET follower = '{}'".format(follower))
		logging.info("New follower added to DB")

	### NEW COMMAND TESTING
	def db_check_command_exists(self, command):
		command = self.db.execute("SELECT content FROM commands WHERE command = '{}'".format(command))
		check_command = self.db.fetchone()
		if(check_command == None):
			return False
		else:
			return True

	def db_add_command(self, command, content):
		if(self.db_check_command_exists(command)):
			return "Error: Command {} already exists OMGScoots".format(command)
		else:
			self.db.execute("INSERT INTO commands VALUES ('{}', '{}')".format(command, content))
			return "Command !{} was added to the database SeemsGood".format(command)

	def db_edit_command(self, command, new_content):
		if(self.db_check_command_exists(command)):		
			self.db.execute("UPDATE commands SET content='{}' WHERE command = '{}'".format(new_content, command))
			return "Command !{} was successfully updated SeemsGood".format(command)
		else:
			return "Error: Command {} doesn't exist OMGScoots".format(command)

	def db_delete_command(self, command):
		if(self.db_check_command_exists(command)):	
			self.db.execute("DELETE FROM commands WHERE command = '{}'".format(command))
			return "Command !{} was successfully deleted KAPOW".format(command)
		else:
			return "Error: Command {} doesn't exist OMGScoots".format(command)

	def db_get_command(self, command, user):
		self.db.execute("SELECT content FROM commands WHERE command = '{}'".format(command))
		response = self.db.fetchone()
		parsed_response = self.db_tuple_to_string(response[0])
		if '<user>' in str(parsed_response):
			parsed_response = parsed_response.replace('<user>', user)
		return parsed_response