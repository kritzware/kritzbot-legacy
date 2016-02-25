import socket
import string
import time

# external py files
from settings import twitch_irc

def openSocket():

	s = socket.socket()
	#w = socket.socket()
	s.connect((twitch_irc.get('HOST'), twitch_irc.get('PORT')))
	s.send(bytes("PASS " + twitch_irc.get('PASS') + "\r\n", 'UTF-8'))
	s.send(bytes("NICK " + twitch_irc.get('NICK') + "\r\n", 'UTF-8'))
	s.send(bytes("JOIN #" + twitch_irc.get('CHANNEL') + "\r\n", 'UTF-8'))

	#s.send(bytes("JOIN #" + twitch_irc.get('GROUPCHAT') + "\r\n", 'UTF-8'))

	return s

def sendMessage(s, message):

	messageTemp = "PRIVMSG #" + twitch_irc.get('CHANNEL') + " :" + message
	s.send(bytes(messageTemp + "\r\n", 'UTF-8'))
	print("Sent: " + messageTemp)