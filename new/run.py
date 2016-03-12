import threading
from threading import Thread
import logging, coloredlogs

from modules.bot import Bot
from modules.whisperconnection import WhisperConnection
from modules.config import *

coloredlogs.install()

logging.info("Instance of bot created..")
logging.info("Hello world!")

bot = Bot(HOST, PORT, PASS, NICK, CHANNEL)
# whisper_bot = WhisperConnection(W_HOST, W_PORT, PASS, NICK, W_GROUP)

if __name__ == '__main__':
	Thread(target=bot.connection).start()
	# Thread(target=whisper_bot.connection).start()