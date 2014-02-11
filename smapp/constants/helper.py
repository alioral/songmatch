import requests
import traceback
import integers
import strings

from collections import defaultdict
from datetime import datetime

from smproject import settings

def is_none(obj): # added in case of additional checks that would be count as none
	return (obj is None)

def get_value_from_dict(key, dictionary):
	if key in dictionary:
		return dictionary[key]
	return None

def log(function_name, message):
	print str(datetime.now()) + ' [' + function_name + '] ' + message
	db['log'].insert({'function':function_name, 
		'log':message, 
		'created_at': datetime.now()})

def get_user_recent_tracks(name):
	recent_track_list = list()
	try:
		response = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + name 
			+ '&api_key=' + settings.API_KEY_LAST_FM + '&format=json')
		
		if is_none(response):
			return recent_track_list

		response_data = response.json()
		recent_tracks = get_value_from_dict('recenttracks', response_data)
		recent_track_list = get_value_from_dict('track', recent_tracks)

	except Exception, e:
		log('get_user_recent_tracks', str(e))

	return recent_track_list

def group_tracks_by_date(recent_tracks):

	timeline = defaultdict(lambda:list())
	
	try:

		for track in recent_tracks:
			date_and_time = get_value_from_dict('date', track)

			if not date_and_time:
				continue

			date_and_time_text = get_value_from_dict('#text', date_and_time)
			date = date_and_time_text.split(',')[0]
			timeline[date].append(track['name'])

	except Exception, e:
		print traceback.format_exc()
		log('group_tracks_by_date', str(e))
	return timeline

def get_matching_song_count(songs_user, songs_country):
	match_rate = 0
	for song in songs_user:
		if song in songs_country:
			match_rate = match_rate + 1	

	return match_rate

def get_top_tracks(country):
	top_track_list = list()
	try:
		response = requests.get('http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=' 
			+ country + '&api_key=' + settings.API_KEY_LAST_FM + '&format=json')
		
		if is_none(response):
			return top_track_list

		response_data = response.json()

		top_tracks = get_value_from_dict('toptracks', response_data)
		top_track_list = get_value_from_dict('track', top_tracks)

	except Exception, e:
		log('get_top_tracks', str(e))

	return top_track_list

def match_songs_with_country(songs_user, countries_and_top_songs):
	max_match_rate = 0
	selected_country = strings.DEFAULT_COUNTRY
	for country in countries_and_top_songs:
		temp_match_rate = get_matching_song_count(songs_user, 
			countries_and_top_songs[country])
		if temp_match_rate > max_match_rate:
			max_match_rate = temp_match_rate
			selected_country = country
	return {'country':selected_country, 'match_rate': max_match_rate}


	