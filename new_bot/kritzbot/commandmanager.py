
from kritzbot.database import DatabaseConnection
from kritzbot.logger import Logger
log = Logger(__name__)

database = DatabaseConnection(__name__)
database.test()

class CommandManager:

	def __init__(self, command, msg, user):
		self.command = command
		self.msg = msg
		self.user = user

	def getCommand(self):
		log.info(self.command)