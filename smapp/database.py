import os

from pymongo import MongoClient

class Database(object):
	_database = None
	def __new__(cls, *args, **kwargs):
		if cls._database is None:
			db_string, db_name = 'mongodb://localhost:27017/', 'songmatch'
			if os.environ.get('MONGOLAB_URI'):
				db_string = os.environ.get('MONGOLAB_URI')
				db_name = 'heroku_app22127074'
			client = MongoClient(db_string)
			cls._database = client[db_name]
		return cls._database