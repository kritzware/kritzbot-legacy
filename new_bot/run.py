#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kritzbot.bot import Bot
from kritzbot.configloader import Bot_Config

bot = Bot(Bot_Config['host'], Bot_Config['port'], Bot_Config['pass'], Bot_Config['nick'], Bot_Config['channel'])

if __name__ == '__main__':
	bot.connectChannel()