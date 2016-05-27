import logging, coloredlogs
import re

from modules.config import *
from modules.database import Database
from modules.api import API

from websocket import create_connection
from urllib.parse import urlparse, parse_qs

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class SongRequest:

	CommandMain = ''
	CommandMainOptions = ['songrequest', 'sr']
	CommandResponses = []

	def __init__(self, user, request):
		self.user = user
		self.request = request
		self.api = API(1)

	def execute_command(self, command):
		from modules.bot import bot_msg

		print("Link:", self.request)
		youtube_id = self.get_link_id(self.request)
		print("ID:", youtube_id)

		# if(database.db_add_song_request(youtube_id, self.user)):
		response = self.get_song_request(youtube_id)
		bot_msg(response)

		# send to db:
		# user, id, timestamp, position (get this on insert)

		# test stuff
		# ws = create_connection("ws://localhost:3001", subprotocols=["echo-protocol"])
		# print("Sending 'Hello world!'")
		# ws.send("Hello, world!")

	def get_song_request(self, id):
		data = self.api.getJSON('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={}&format=json'.format(id))
		song_title = data['title']
		# return "{} added {} to the playlist VaultBoy".format(self.user, song_title)
		return "{} was added to the playlist (requested by {}) VaultBoy".format(song_title, self.user)

	def get_link_id(self, url):
		""" Credit to https://gist.github.com/kmonsoor/2a1afba4ee127cce50a0

		Examples of URLs:
      	Valid:
	        'http://youtu.be/_lOT2p_FCvA',
	        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
	        'http://www.youtube.com/embed/_lOT2p_FCvA',
	        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
	        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
	        'youtube.com/watch?v=_lOT2p_FCvA',
      
      	Invalid:
        	'youtu.be/watch?v=_lOT2p_FCvA', """

		if url.startswith(('youtu', 'www')):
			url = 'http://' + url

		query = urlparse(url)

		if 'youtube' in query.hostname:
			if query.path == '/watch':
				return parse_qs(query.query)['v'][0]
			if query.path.startswith(('/embed', '/v')):
				return query.path.split('/')[2]
		if 'youtu.be' in query.hostname:
			return query.path[1:]
		else:
			raise ValueError