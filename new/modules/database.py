import pymysql
import re
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
		connection = pymysql.connect(
			host = self.host,
			user = self.user,
			password = self.password,
			db = self.name,
			autocommit = self.autocommit
		)
		db = connection.cursor()
		return db

	def db_test(self):
		self.db.execute("UPDATE table1 set points = points + 1")
		return "added points to db"

	

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()