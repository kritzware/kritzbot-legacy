import pymysql
import string
import re

from kritzbot.configloader import BotCfg
from kritzbot.logger import Logger
log = Logger(__name__)

class DatabaseConnection:

	def __init__(self, name):
		self.name = name
		log.info('Database connection created at {}'.format(self.name))
		self.db = self.createDatabaseConnection()

	def createDatabaseConnection(self):
		connection = pymysql.connect(
				host = BotCfg.cfg('sql:host'),
				user = BotCfg.cfg('sql:user'),
				password = BotCfg.cfg('sql:pass'),
				db = BotCfg.cfg('sql:database'),
				autocommit = True,
				charset = 'utf8'
			)
		return connection.cursor()

	def closeDatabaseConnection(self):
		self.db.close()
		log.info('Database connection closed.')
		
	def test(self):
		self.db.execute('SELECT * FROM points')
		data = self.db.fetchall()
		print(data)
		self.closeDatabaseConnection()