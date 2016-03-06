import json
import urllib.request
import re

from datetime import datetime, timedelta, date, time
from modules.settings import twitch_irc
from modules.temp import latest_follower, new_follower_found

songlist_list = []

def getJSON(url):

	request = urllib.request.urlopen(url)
	data = json.loads(request.read().decode('UTF-8'))
	return data

def getJSON_text(url):

	request = urllib.request.urlopen(url)
	data = request.read()
	data_string = data.decode('UTF-8')
	return data_string

def getJSON_youtube(url):

	json_obj  = urllib.request.urlopen(url).read().decode('UTF-8')
	json_list = json.loads(json_obj)
	return json_list

def check_user_class(user, user_class):

	try:
		data = getJSON('https://tmi.twitch.tv/group/user/' + twitch_irc.get('CHANNEL') + '/chatters')
		chatters = data['chatters'][user_class]

		print("[DEBUG] >>> " + str(user_class) + " IN CHAT >>> ", chatters)

		for n in chatters:
			
			print("[DEBUG] >>> CHECKING >>> ", n)

			if(n == user):
				print("[INFO] >>> " + user + " found in class " + user_class)
				return(True)

	except urllib.error.URLError as e:
		print("[ERROR] >>> ", e.reason)
		return("Error: Twitch API down BabyRage")

def get_users_json_viewers():
	try:
		data = getJSON('https://tmi.twitch.tv/group/user/' + twitch_irc.get('CHANNEL') + '/chatters')
		chatters = data['chatters']['viewers']
		return chatters
	except urllib.error.URLError as e:
		print("[ERROR] >>> ", e.reason)

def get_users_json_mods():
	try:
		data = getJSON('https://tmi.twitch.tv/group/user/' + twitch_irc.get('CHANNEL') + '/chatters')
		chatters = data['chatters']['moderators']
		return chatters
	except urllib.error.URLError as e:
		print("[ERROR] >>> ", e.reason)

def get_latest_highlight(info):

	try:
		data = getJSON('https://api.twitch.tv/kraken/channels/' + twitch_irc.get('CHANNEL') + '/videos?limit=1')

		return_data = data['videos'][0][info]
		return return_data
	except urllib.error.URLError as e:
		print("[ERROR] >>> ", e.reason)

def get_latest_follower():

	# data = getJSON("https://api.twitch.tv/kraken/channels/" + twitch_irc.get('CHANNEL') + "/follows/?limit=1")
	# follower = data["follows"][0]['user']['name']
	# latest_follower.append(follower)

	# print("[INFO] >>> Latest follower >>> ", latest_follower)

	# if(follower == latest_follower[0]):
	# 	print("No new follower detected")


	# for n in latest_follower:
	# 	if n != follower:
	# 		latest_follower.pop(0)
	# 		latest_follower.append(follower)
	# 		print("New follower added!")
	# else:
	# 	print("checking for new follower in 60 secs")
	data = getJSON("https://api.twitch.tv/kraken/channels/" + twitch_irc.get('CHANNEL') + "/follows/?limit=1")

	#test follower	
	new_follower = "meme_boy69"

	if(len(latest_follower) == 0):
		follower = data["follows"][0]['user']['name']
		latest_follower.append(follower)
		print("[INFO] >>> Latest follower >>> ", latest_follower)
		new_follower_found = True
	else:
		# new_follower = data["follows"][0]['user']['name']
		if(new_follower not in latest_follower):
			latest_follower.pop(0)
			latest_follower.append(new_follower)
			output = ("[INFO] >>> New follower >>> ", new_follower)
			print("new follower found!")
			new_follower_found = True
			return str(new_follower)
		# print("no new follower found")
		print("no new follower found!")
		new_follower_found = False
	# print("no new follower found")
	new_follower_found = False
	return "no new follower found"

def get_youtube_id(url):

	video_id = re.search(r'\?(.*)', url).group()
	output = video_id[3:]
	return output

def get_youtube_request(user, url):

	video_id = get_youtube_id(url)
	# print("[DEBUG] >>> VIDEO ID >>>", video_id)
	get_url = 'https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={}&format=json'.format(video_id)
	# print("[DEBUG] >>> URL TO RETRIEVE ", str(get_url))

	data = getJSON_youtube('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=jt0bdaeZMVQ&format=json')
	video_title = data['title']

	songlist_list.append(video_id)
	add_to_queue(video_id[0])
	songlist_list.pop(0)
	print(songlist_list)
	output = "'{}' has been added to the queue, {} SeemsGood".format(video_title, user)
	return output

def add_to_queue(video_id):

	# with open('modules/songlist.json', 'w') as json_file:
	# 	json_file.write("{}\n".format(json.dumps(songlist_list)))

	with open('modules/songlist.json', 'a') as json_file:
		json_file.write("{}\n".format(json.dumps(songlist_list[0])))
	print(songlist_list)

	# with open('modules/songlist.json', 'w+') as outfile:
	# 	print(video_id)
	# 	json.dump(video_id, outfile)
	# print("SONG STORED IN JSON FILE")