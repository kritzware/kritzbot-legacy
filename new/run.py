import logging, coloredlogs

from modules.bot import Bot
from modules.config import *

coloredlogs.install()

logging.info("Instance of bot created..")
logging.info("Hello world!")

bot = Bot(HOST, PORT, PASS, NICK, CHANNEL)
bot.connection()