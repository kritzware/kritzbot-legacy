import string
import threading

from TheSocket import sendMessage
from Commands import commands
from Read import add_points

def joinRoom(s):
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	sendMessage(s, "/me has booted up, joining chat MrDestructoid")
	
	def auto_message():
		threading.Timer(600, auto_message).start()
		sendMessage(s, commands.get('twitter'))
	auto_message()

	def points_timer():
		threading.Timer(60, points_timer).start()
		add_points()
	points_timer()
	
def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True