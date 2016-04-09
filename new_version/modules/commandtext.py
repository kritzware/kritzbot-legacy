from modules.config import *

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
	'gn': 'Goodnight <param2> OpieOP OpieOP',
	'kritz': 'RAFFLE BabyRage KRITZWARE, RAFFLE BabyRage WE WANT RAFFLE KRITZ BabyRage',
	'fu': 'Hey <param2> ( ° ͜ʖ͡°)╭∩╮',
	'hug': '<user> hugs <param2> (っಠ‿ಠ)っ <3 <3',
	'currency': 'You gain points by watching the stream. Check how many you have with !points, or gamble them away with !roulette Kappa'
}

# advanced_commands = {
# 	'points': database.db_get_points_user,
# 	'rank': database.db_get_user_rank,
# }
advanced_commands = ['rank',
					 'points',
					 'uptime',
					 'localtime',
					 'playsound',
					 'roulette',
					 'raffle',
					 'join',
					 'test'
					]

# friends = {
# 	'acorn': 'You should (definitely) go check out the lovely AcornBandit over at twitch.tv/acornbandit RaccAttack',
# 	'geek': 'You should (definitely) go check out the lovely GeekGeneration over at twitch.tv/thegeekgeneration Poooound',
# }

# quotes = ['"rebound it like your last relationship!" - skowalz 2k16', ]

auto_messages = ['Make sure to follow {} on twitter for the latest updates! {}'.format(CHANNEL, TWITTER),
 				 'Check out the latest highlights here! twitch.tv/{}/profile/highlights'.format(CHANNEL), 
 				 'Make sure to follow the channel to get notified of the latest streams!',
 				]