import string
from TheSocket import sendMessage
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
	
def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True