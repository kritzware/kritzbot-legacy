# external py files
from irc_socket import openSocket, sendMessage

# connection to the irc server is created
s = openSocket()
joinRoom(s)
readbuffer = ""

while True:
	readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
	temp = str.split(readbuffer, "\n")
	readbuffer = temp.pop()

	for line in temp:
		print(line)

		# reply to ping request with pong
		if "PING :tmi.twitch.tv" in line:
			response = "PONG :tmi.twitch.tv"
			bytes_response = str.encode(response)
			s.send(bytes_response)
			break

		# commands are executed below