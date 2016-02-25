import socket

if __name__ == "__main__":
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('127.0.0.1', 8080))

	client.sendall(bytes("This is a message from the python!", 'UTF-8'))
	data = client.recv(1024)
	client.close()

	print('Received data', repr(data))