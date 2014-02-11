import requests

from collections import defaultdict

from database import Database

from constants.helper import get_user_recent_tracks
from constants.helper import is_none
from constants.helper import get_top_tracks
from constants.helper import get_value_from_dict

from constants.lists import COUNTRY_LIST


db = Database()

class User:

	def __init__(self, name):
		self.name = name

	def get_recent_tracks(self):
		if not hasattr(self, 'recent_tracks'):
			self.recent_tracks = get_user_recent_tracks(self.name)
			db['user'].insert({'username':self.name, 
				'recent_tracks': self.recent_tracks})

		return self.recent_tracks

class Country():

	countries_and_top_tracks = None

	@staticmethod
	def get_countries_and_top_songs():

		if is_none(Country.countries_and_top_tracks):
			Country.countries_and_top_tracks = defaultdict(lambda:list())
			
			for country in COUNTRY_LIST:
				country_top_tracks = get_top_tracks(country)
				for top_track in country_top_tracks:
					track_name = get_value_from_dict('name', top_track)
					if is_none(track_name):
						continue
					Country.countries_and_top_tracks[country].append(track_name)

		return Country.countries_and_top_tracks
			

    	












