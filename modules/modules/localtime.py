import logging, coloredlogs
from datetime import datetime, timedelta, date, time
from pytz import timezone
from modules.config import *

class LocalTime:

	CommandMain = 'localtime'
	CommandResponses = []
	
	def __init__(self):
		self.channel = CHANNEL

	def execute_command(self, command):
		self.local_time()

	def local_time(self):
		from modules.bot import bot_msg
		localtime = timezone(str(TIME_ZONE))
		time = datetime.now(localtime)
		format_time = time.strftime('%H:%M:%S')
		if TIME_ZONE == 'US/Eastern':
			output = "Local time: {} EST".format(format_time)
		if TIME_ZONE == 'Europe/London':
			output = "Local time: {} GMT".format(format_time)
		if TIME_ZONE == 'Europe/Oslo':
			output = "Local time: {} CEST".format(format_time)
		bot_msg(output)		