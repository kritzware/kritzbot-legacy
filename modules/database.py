import pymysql
import re
import string
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
			autocommit = self.autocommit,
			charset = 'utf8'
		)
		db = connection.cursor()
		return db

	def db_close(self):
		return self.db.close()

	def db_format(self, data):
		format_data = re.findall('[+-]?\d+(?:\.\d+)?', str(data))
		return format_data[0]

	def db_tuple_to_string(self, data):
		return ''.join(data)

	def db_add_user(self, user):
		self.db.execute("INSERT ignore into points VALUES ('{}', 0)".format(user))

	def db_add_points_user(self, user, points):
		self.db.execute("UPDATE points set points = points + {} where user_id = '{}'".format(points, user))

	def db_minus_points_user(self, user, points):
		self.db.execute("UPDATE points set points = points - {} where user_id = '{}'".format(points, user))

	def db_check_user_exists(self, user):
		points = self.db.execute("SELECT user_id FROM points where user_id = '{}'".format(user))
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
			if(user != self_user):
				output = "{} has {} {}".format(user, points, CURRENCY)
		return output

	def db_get_user_points_int(self, user):
		points = self.db.execute("SELECT points from points where user_id = '{}'".format(user))
		get_points = self.db.fetchone()
		#if(get_points == None):
		#	self.db_add_user(user)
		#	points = self.db.execute("SELECT points from points where user_id = '{}'".format(user))
		#	get_points = self.db.fetchone()
		return int(self.db_format(get_points))

	def db_get_user_total(self):
		self.db.execute("SELECT COUNT(*) AS user_id FROM points")
		user_total = self.db.fetchone()
		format_user_total = self.db_format(str(user_total))
		return(str(format_user_total))

	def db_get_user_rank(self, user):
		user = self.bttv_parse(user)
		#try:
		self.db.execute("SELECT 1 + (SELECT count(*) FROM points a WHERE a.points > b.points ) AS rank FROM points b WHERE user_id = '{}' ORDER BY rank LIMIT 1".format(user))
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

	# DUEL QUERIES

	def db_add_duel(self, user, opponent, amount):
		self.db.execute("INSERT INTO duels VALUES ('{}', '{}', {}, NOW())".format(user, opponent, amount))

	def db_check_duel_exists_user(self, user):
		check_duel = self.db.execute("SELECT user FROM duels WHERE user = '{}'".format(user))
		check_duel_user = self.db.fetchone()
		if(check_duel_user == None):
			return False
		else:
			return True

	def db_check_duel_exists_opponent(self, user):
		check_duel = self.db.execute("SELECT opponent FROM duels WHERE opponent = '{}'".format(user))
		check_duel_user = self.db.fetchone()
		if(check_duel_user == None):
			return False
		else:
			return True

	def db_get_duel_user_from_opponent(self, user):
		self.db.execute("SELECT user FROM duels WHERE opponent = '{}'".format(user))
		opponent = self.db.fetchall()
		opponent_parsed = self.db_tuple_to_string(opponent[0])
		return opponent_parsed

	def db_get_duel_opponent_from_user(self, user):
		self.db.execute("SELECT opponent FROM duels WHERE user = '{}'".format(user))
		opponent = self.db.fetchall()
		opponent_parsed = self.db_tuple_to_string(opponent[0])
		return opponent_parsed

	def db_get_duel_amount(self, user):
		self.db.execute("SELECT amount FROM duels WHERE opponent = '{}'".format(user))
		get_amount = self.db.fetchone()
		return int(self.db_format(get_amount))

	def db_remove_duel(self, user):
		self.db.execute("DELETE FROM duels WHERE opponent = '{}'".format(user))

	def db_duel_expired(self):
		val = int(DUEL_EXPIRE / 60)
		self.db.execute("DELETE FROM duels WHERE time < (NOW() - INTERVAL {} MINUTE)".format(val))


	### NEW COMMAND TESTING
	def db_check_command_exists(self, command):
		command = self.db.execute("SELECT content FROM commands WHERE command = '{}'".format(command))
		check_command = self.db.fetchone()
		if(check_command == None):
			return False
		else:
			return True

	def db_add_command(self, command, content, user):
		if(self.db_check_command_exists(command)):
			return False
		else:
			print(content)
			command = command.replace("'", "\'")
			self.db.execute('INSERT INTO commands VALUES ("{}", "{}")'.format(command, str(content)))
			return True

	def db_edit_command(self, command, new_content, user):
		if(self.db_check_command_exists(command)):		
			self.db.execute("UPDATE commands SET content='{}' WHERE command = '{}'".format(new_content, command))
			return True
		else:
			return False

	def db_delete_command(self, command, user):
		if(self.db_check_command_exists(command)):	
			self.db.execute("DELETE FROM commands WHERE command = '{}'".format(command))
			return True
		else:
			return False

	def db_get_command(self, command, user):
		self.db.execute("SELECT content FROM commands WHERE command = '{}'".format(command))
		response = self.db.fetchone()
		parsed_response = self.db_tuple_to_string(response[0])
		if '{user}' in str(parsed_response):
			parsed_response = parsed_response.replace('{user}', user)
		return parsed_response

	def db_add_song_request(self, song_id, user):
		print(song_id)
		print(user)
		try:
			self.db.execute("INSERT INTO song_requests VALUES ('{}', '{}', NOW())".format(song_id, user))
			return True
		except:
			return False