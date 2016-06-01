#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kritzbot.bot import Bot

# Bot IRC/Chat connection
HOST = "irc.chat.twitch.tv"
PORT = 6667
PASS = "oauth:tr5ucth56bckyltuv6gek0i0705tka"
NICK = "kritzbot"
CHANNEL = "kritzware"

bot = Bot(HOST, PORT, PASS, NICK, CHANNEL)

if __name__ == '__main__':
	bot.connectChannel()