import json
import os

from kritzbot.logger import Logger
log = Logger(__name__)

config_dir = os.path.dirname(__file__)
file_path = os.path.join(config_dir, '../bot_config.json')

class ConfigLoader:

	def __init__(self, __file__):
		log.info('Bot config loaded at {}'.format(__file__))
		self.hashes = []
		with open(file_path, 'r') as bot_config:
			self.config = json.load(bot_config)

	def cfg(self, data):
		self.hashes[:] = []
		for i in range(2):
			hash = data.split(':', 1)[i]
			self.hashes.append(hash)
		return self.config[self.hashes[0]][self.hashes[1]]

BotCfg = ConfigLoader(__file__)
Bot_Config = {
	'host': BotCfg.cfg('twitch:host'),
	'port': BotCfg.cfg('twitch:port'),
	'pass': BotCfg.cfg('twitch:pass'),
	'nick': BotCfg.cfg('twitch:nick'),
	'channel': BotCfg.cfg('twitch:channel')
}