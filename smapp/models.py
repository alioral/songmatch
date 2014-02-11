import requests

from collections import defaultdict

from constants.helper import get_user_recent_tracks
from constants.helper import is_none
from constants.helper import get_top_tracks
from constants.helper import get_value_from_dict

from constants.lists import COUNTRY_LIST

class User:

	def __init__(self, name):
		self.name = name

	def get_recent_tracks(self):
		if not hasattr(self, 'recent_tracks'):
			self.recent_tracks = get_user_recent_tracks(self.name)
		return self.recent_tracks

	def get_neighbours(self):

		if not hasattr(self, 'neighbours'):
			self.neighbours = get_user_neighbours(self.name)
		return self.neighbours

	def compare_with(self, neighbour):
		result = compare_users(self.name, neighbour)
		return result

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
			

    	












