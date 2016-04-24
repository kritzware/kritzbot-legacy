import logging, coloredlogs
from threading import Thread
from random import choice 
from time import sleep

from modules.config import *
from modules.api import API

class Giveaway:

	GiveawayActive = False
	GiveawayEntries = []

	def __init__(self, time, prize):
		self.time= time
		self.prize = prize
		self.api = API(1)
		self.time_seconds = self.time * 60

	def start_giveaway(self):
		from modules.bot import bot_msg, bot_msg_whsp
		bot_msg("The giveaway for {} has started. Type !enter to join. You have {} minutes! PogChamp".format(self.prize, self.time))
		
		for viewers in self.api.get_viewers_json('viewers'):
			print(viewers)
			bot_msg_whsp("A giveaway has started for {}. Type !enter in the main chat to join. You have {} minutes!".format(self.prize, self.time), viewers)
		for mods in self.api.get_viewers_json('moderators'):
			bot_msg_whsp("A giveaway has started for {}. Type !enter in the main chat to join. You have {} minutes!".format(self.prize, self.time), mods)

		Giveaway.GiveawayActive = True	
		Thread(target=self.giveaway_win).start()
		return ""

	def giveaway_win(self):
		from modules.bot import bot_msg_whsp, bot_msg
		amount_mins = int(self.time / 2)
		amount = int(self.time_seconds / 2)
		sleep(amount)
		bot_msg("The giveaway ends in {} minutes. Type !enter to join".format(amount_mins))
		sleep(amount)
		if(len(Giveaway.GiveawayEntries) == 0):
			bot_msg("Nobody entered the giveaway LUL")
			return ""
		winner = choice(Giveaway.GiveawayEntries)
		bot_msg("And the winner is...")
		sleep(2)
		bot_msg("PogChamp PogChamp {} PogChamp PogChamp".format(winner))
		bot_msg_whsp("You won the giveaway, make sure you type someting in chat to prove you're still here!", winner)
		self.giveaway_clear()

	def giveaway_clear(self):
		Giveaway.GiveawayActive = False
		del Giveaway.GiveawayEntries[:]