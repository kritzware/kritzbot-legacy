from datetime import datetime, timedelta, date, time
from pytz import timezone
from modules.config import *
from modules.api import API

streamOnlineCheck = API(1)

class Time:

	def __init__(self):
		self.channel = CHANNEL

	def uptime(self):
		if streamOnlineCheck.check_stream_online():
			data = streamOnlineCheck.getJSON('https://api.twitch.tv/kraken/channels/{}/videos?limit=1&broadcasts=true'.format(self.channel))
			latest_stream = data['videos'][0]['recorded_at']
			
			timeformat = "%Y-%m-%dT%H:%M:%SZ"
			start_date = datetime.strptime(latest_stream, timeformat)
			current_date = datetime.utcnow()
			output_date = current_date - start_date - timedelta(microseconds=current_date.microsecond)
			
			hours = str(output_date)[:1]
			minutes = str(output_date)[2:4]
			
			return "{} has been live for {} hrs, {} mins FeelsGoodMan".format(self.channel, hours, minutes) 
		else:
			return "{} is not streaming at the moment FeelsBadMan".format(self.channel)

	def local_time(self):
		localtime = timezone(str(TIME_ZONE))
		time = datetime.now(localtime)
		format_time = time.strftime('%H:%M:%S')
		if TIME_ZONE == 'US/Eastern':
			output = "Local time: {} EST".format(format_time)
		if TIME_ZONE == 'Europe/London':
			output = "Local time: {} GMT".format(format_time)
		return output