from modules.database import Database
from modules.config import *
from modules.api import API

api = API(5)

commands = {
	'github': 'Report an issue or suggest ideas at github.com/kritzware/kritzbot 4Head',
	'wut': ' Alwaaaays waaaatchiiiiing~ ( ͡° ͜ʖ ͡°)',
	'robot': 'I\'m not real.. FeelsBadMan',
	'spooky': 'Hold me chat, I\'m scared! WutFace WutFace WutFace',
	'help': '<user>, you can view my commands here: {} MrDestructoid'.format(COMMAND_LINK),
	'doggy': 'EleGiggle doggyfood has lost 1647359 points EleGiggle',
	'donger': 'ᕙ༼ຈل͜ຈ༽ᕗ. ʜᴀʀᴅᴇʀ,﻿ ʙᴇᴛᴛᴇʀ, ғᴀsᴛᴇʀ, ᴅᴏɴɢᴇʀ .ᕙ༼ຈل͜ຈ༽ᕗ',
	'twitter': 'Make sure to follow {} on twitter for the latest updates! {} OMGScoots'.format(CHANNEL, TWITTER),
	'merch': 'Want to support the stream AND get some cool loot? Grab some merch here! {} KappaPride'.format(MERCH),
	'coloring': 'Grab a coffee & ease into the day KappaRoss Expect me here weekday mornings from about 6:15AM - 7:00AM EST. Dope-ass coloring pages from etsy.me/1KbIzqO',
	'rigged': 'DansGame RIGGED DansGame RIGGED DansGame',
	'discord': 'Chat with other viewers on discord! {} MingLee'.format(DISCORD),
	'raid': 'SKOWALZ SQUALL PogChamp PogChamp',
	'hype': 'PogChamp PogChamp PogChamp',
	'chatlove': 'CHAT LOOOVE bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple bleedPurple',
	'nice': '☑ Stream online ☑ Earning points ☑ KappaPride in chat - Must be SKOWALZ stream FeelsGoodMan',
	'kritz': 'RAFFLE BabyRage KRITZWARE, RAFFLE BabyRage WE WANT RAFFLE KRITZ BabyRage',
	'fu': 'Hey <param2> ( ° ͜ʖ͡°)╭∩╮',
	'hug': '<user> hugs <param2> (っಠ‿ಠ)っ <3 <3',
	'test': '<user> <param2> <param3>'
}

# advanced_commands = {
# 	'points': database.db_get_points_user,
# 	'rank': database.db_get_user_rank,
# }
advanced_commands = ['points',
					 'rank',
					]

test_commands = ['points',
				 'rank',
				]

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

auto_messages = ['Make sure to follow SKOWALZ on twitter for the latest updates! {}'.format(TWITTER),
 				 'Check out the latest highlights here! twitch.tv/{}/profile/highlights'.format(CHANNEL), 
 				 'Make sure to follow the channel to get notified of the latest streams!',
 				]

# def chat_auto_messages():

# 	output = random.choice(auto_messages)
# 	return str(output)