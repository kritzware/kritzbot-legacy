import threading
from threading import Thread
import logging, coloredlogs

from modules.bot import Bot
from modules.config import *
from modules.timer import Timer

coloredlogs.install()

logging.info("Instance of bot created..")
logging.info("{} spawned: Hello world!".format(NICK))

bot = Bot(HOST, PORT, PASS, NICK, CHANNEL)

if __name__ == '__main__':
	# Thread(target=bot.connection).start()
	bot.connection()