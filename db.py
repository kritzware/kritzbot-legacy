from pymongo import MongoClient
from Commands import database

def databaseConnection():
	client = MongoClient(database)
	print("Connection to database..")
	print("Connected to: " + database[33:])

databaseConnection()