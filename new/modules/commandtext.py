from modules.database import database
from modules.config import *

commands = {
	'github': 'Report an issue or suggest ideas at github.com/kritzware/pybot 4Head',
	'wut': ' Alwaaaays waaaatchiiiiing~ ( ͡° ͜ʖ ͡°)',
	'bot': 'I\'m not real.. FeelsBadMan',
}
user_commands = {
	'help': ', you can view my commands here: [add-link] MrDestructoid'
}
advanced_commands = {
	'test': database.db_test
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