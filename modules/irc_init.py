import string
import threading

# external py files
from modules.irc_socket import sendMessage

version = "version 1.2"

def joinRoom(s):

	readbuffer = ""
	loading = True
	while loading:

		readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for line in temp:
			print(line)
			loading = loadingComplete(line)

	# sends message on join
	# sendMessage(s, " joined the channel, running on {}".format(version))

def loadingComplete(line):

	if("End of /NAMES list" in line):
		return False
	else:
		return True