import json
import urllib.request

from datetime import datetime, timedelta, date, time

def getJSON(url):

	request = urllib.request.urlopen(url)
	data = json.loads(request.read().decode('UTF-8'))
	return data

def getJSON_text(url):

	request = urllib.request.urlopen(url)
	data = request.read()
	data_string = data.decode('UTF-8')
	return data_string