import threading
from threading import Thread
import logging, coloredlogs

from modules.bot import Bot
from modules.whisperconnection import WhisperConnection
from modules.config import *
from modules.timer import Timer

coloredlogs.install()

logging.info("Instance of bot created..")
logging.info("Hello world!")

bot = Bot(HOST, PORT, PASS, NICK, CHANNEL)

if __name__ == '__main__':
	Thread(target=bot.connection).start()
	# Thread(target=whisper_bot.connection).start()
	# Thread(target=points_timer.run).start()
	# points_timer.auto()