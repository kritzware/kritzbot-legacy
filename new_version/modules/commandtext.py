from modules.database import Database
from modules.config import *
from modules.api import API

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()
api = API(5)

commands = {
	'github': 'Report an issue or suggest ideas at github.com/kritzware/kritzbot 4Head',
	'wut': ' Alwaaaays waaaatchiiiiing~ ( ͡° ͜ʖ ͡°)',
	'robot': 'I\'m not real.. FeelsBadMan',
	'spooky': 'Hold me chat, I\'m scared! WutFace WutFace WutFace'
}
user_commands = {
	'help': ', you can view my commands here: {} MrDestructoid'.format(COMMAND_LINK)
}
advanced_commands = {
	'points': database.db_get_points_user,
	'rank': database.db_get_user_rank,
}
api_commands = {
	'test': api.get_latest_follower
}

# commands_old = {
# 	'admin': 'Contact Kritzware if you have any queries or wish to report bugs 4Head',
# 	'help': ', you can view my commands here: https://github.com/LouisBluhm/PyBot#readme MrDestructoid',
# 	'twitter': 'Make sure to follow Skowalz on twitter for the latest updates! twitter.com/skowalz PogChamp',
# 	'spooky': "Hold me chat, I'm scared! WutFace WutFace WutFace",
# 	'donger': 'ᕙ༼ຈل͜ຈ༽ᕗ. ʜᴀʀᴅᴇʀ,﻿ ʙᴇᴛᴛᴇʀ, ғᴀsᴛᴇʀ, ᴅᴏɴɢᴇʀ .ᕙ༼ຈل͜ຈ༽ᕗ',
# 	'bot': "I'm not real.. FeelsBadMan",
# 	'vampire': "Imma suck your blood ~ Keepo ~",
# 	'wut': " Alwaaaays waaaatchiiiiing~ ( ͡° ͜ʖ ͡°)",
# 	'rigged': "DansGame RIGGED DansGame RIGGED DansGame",
# 	'raid': "SKOWALZ SQUALL PogChamp PogChamp"
# }

# update_commands = {
# 	'coloring': 'Grab a coffee & ease into the day :) Expect me here weekday mornings from about 6:15AM - 7:00AM EST. Dope-ass coloring pages from >> http://etsy.me/1KbIzqO'
# }

# friends = {
# 	'acorn': 'You should (definitely) go check out the lovely AcornBandit over at twitch.tv/acornbandit RaccAttack',
# 	'geek': 'You should (definitely) go check out the lovely GeekGeneration over at twitch.tv/thegeekgeneration Poooound',
# }

# quotes = ['"rebound it like your last relationship!" - skowalz 2k16', ]

# auto_messages = ['Make sure to follow SKOWALZ on twitter for the latest updates! twitter.com/skowalz',
# 'Check out the latest highlights here! twitch.tv/skowalz/profile/highlights', 
# 'Make sure to follow the channel to get notified of the latest streams!']

# def chat_auto_messages():

# 	output = random.choice(auto_messages)
# 	return str(output)