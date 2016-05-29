import logging, coloredlogs
from datetime import datetime, timedelta, date, time
from pytz import timezone
from modules.config import *
from modules.api import API

streamOnlineCheck = API(1)

class Uptime:

	CommandMain = 'uptime'
	CommandMainOptions = []
	CommandResponses = []
	
	def __init__(self):
		self.channel = CHANNEL

	def execute_command(self, command):
		from modules.bot import bot_msg
		if streamOnlineCheck.check_stream_online():
			self.uptime()
		else:
			bot_msg("{} is not streaming at the moment FeelsBadMan".format(self.channel))

	def uptime():
		from modules.bot import bot_msg
		data = streamOnlineCheck.getJSON('https://api.twitch.tv/kraken/channels/{}/videos?limit=1&broadcasts=true'.format(self.channel))
		latest_stream = data['videos'][0]['recorded_at']

		timeformat = "%Y-%m-%dT%H:%M:%SZ"
		start_date = datetime.strptime(latest_stream, timeformat)
		current_date = datetime.utcnow()
		output_date = current_date - start_date - timedelta(microseconds=current_date.microsecond)
			
		hours = str(output_date)[:1]
		minutes = str(output_date)[2:4]

		bot_msg("{} has been live for {} hrs, {} mins FeelsGoodMan".format(self.channel, hours, minutes))