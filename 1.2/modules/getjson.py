import json
import urllib.request

from datetime import datetime, timedelta, date, time

def getJSON(url):

	request = urllib.request.urlopen(url)
	data = json.loads(request.read().decode('UTF-8'))
	return data

# def uptime():

# 	user_channel = CHANNEL
# 	url = 'https://api.twitch.tv/kraken/channels/' + user_channel + '/videos?limit=1&broadcasts=true'
# 	req = urllib.request.urlopen(url)
# 	data = json.loads(req.read().decode('UTF-8'))
# 	latestbroadcast = data['videos'][0]['recorded_at']
# 	online = True

# 	#print("Broadcast start: " + latestbroadcast)

# 	timeformat = "%Y-%m-%dT%H:%M:%SZ"
# 	startdate = datetime.strptime(latestbroadcast, timeformat)
# 	currentdate = datetime.utcnow()
# 	combineddate = currentdate - startdate - timedelta(microseconds=currentdate.microsecond)

# 	check_request = urllib.request.urlopen('https://api.twitch.tv/kraken/streams/' + user_channel)
# 	check_online = json.loads(check_request.read().decode('UTF-8'))
# 	if(check_online['stream'] == None):
# 		online = False

# 	hours = str(combineddate)[:1]
# 	minutes = str(combineddate)[2:4]

# 	if(online):
# 		#print(combineddate)
# 		return("/me " + user_channel + " has been live for " + hours + " hrs, " + minutes + " mins")
# 	else:
# 		return("/me " + user_channel + " is not streaming at the moment FeelsBadMan")