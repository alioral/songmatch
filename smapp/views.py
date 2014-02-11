# Create your views here.
import requests
import json

from django.shortcuts import render
from django.shortcuts import HttpResponse

from constants import strings

from constants.helper import is_none
from constants.helper import group_tracks_by_date
from constants.helper import match_songs_with_country

from models import User
from models import Country

def index(request):
	return render(request, 'index.html')

def find(request):

	
	if request.method == 'GET':
		return HttpResponse('Error')
	

	if 'username' not in request.POST:
		return HttpResponse('Error')

	name = request.POST['username']

	if is_none(name):
		name = strings.DEFAULT_USERNAME

	user = User(name)
	recent_tracks = user.get_recent_tracks()

	if is_none(recent_tracks):
		return HttpResponse('Error')

	tracks_by_date = group_tracks_by_date(recent_tracks)

	if is_none(tracks_by_date):
		return HttpResponse('Error')
	
	countries_and_top_songs = Country.get_countries_and_top_songs()

	song_data = []
	for date in tracks_by_date:
		songs_listened = tracks_by_date[date]
		country_object = match_songs_with_country(songs_listened, 
			countries_and_top_songs)

		song_data.append({'date':date, 'country':country_object['country'], 
			'match_rate':country_object['match_rate']})

	return render(request, 'results.html', {'data':json.dumps(song_data)})