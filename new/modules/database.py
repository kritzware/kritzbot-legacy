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

	def db_add_user(self, user):
		self.db.execute("INSERT ignore into table1 VALUES ('{}', 0)".format(user))

	def db_add_points_user(self, user, points):
		self.db.execute("UPDATE table1 set points = points + {} where user_id = '{}'".format(points, user))

	def db_minus_points_user(self, user, points):
		self.db.execute("UPDATE table1 set points = points - {} where user_id = '{}".format(points, user))

	def db_get_points_user(self, user):
		count = self.db.execute("SELECT * FROM table1")
		self.db.execute("SELECT user_id from table1")
		users = self.db.fetchall()
		for n in range(0, count + 1):

			if users[n] != str(user):
				self.db_add_points_user(user, 0)
				self.db.execute("SELECT points from table1 where user_id = '{}'".format(user))
				get_points = self.db.fetchone()
				format_points = self.db_format(get_points)
				output = "{} has {} points".format(user, format_points)
				if(int(format_points) < 0):
					neg_output = "{} has -{} points BabyRage".format(user, format_points)
					return str(neg_output)
				else:
					return output

			if str(users[n]) == str(user):
				self.db.execute("SELECT points from table1 where user_id = '{}'".format(user))
				get_points = self.db.fetchone()
				format_points = self.db_format(get_points)
				output = "{} has {} points".format(user, format_points)
				return output

	def db_get_user_points_int(self, user):
		points = self.db.execute("SELECT points from table1 where user_id = '{}'".format(user))
		get_points = self.db.fetchone()
		return int(self.db_format(get_points))

	def db_get_user_total(self):
		self.db.execute("SELECT COUNT(*) AS user_id FROM table1")
		user_total = self.db.fetchone()
		format_user_total = self.db_format(str(user_total))
		return(str(format_user_total))

	def db_get_user_rank(self, user):
		try:
			self.db.execute("SELECT 1 + (SELECT count(*) FROM table1 a WHERE a.points > b.points ) AS rank FROM table1 b WHERE user_id = '{}' ORDER BY rank LIMIT 1".format(user))
			ranking = self.db.fetchone()
			format_ranking = self.db_format(ranking)
			format_points = self.db_get_user_points_int(user)
			total_users = self.db_get_user_total()
			output = "You are rank {} out of {} {}, with {} points!".format(str(format_ranking), total_users, user, format_points)
			return output
		except Exception:
			self.db_add_user(user)
			points = self.db_get_user_points_int(user)
			return "You are at the bottom {}, with {} points FeelsBadMan".format(user, points)			

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()