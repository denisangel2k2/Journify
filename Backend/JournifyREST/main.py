import datetime
import os
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import requests
import spotipy
import urllib
import json
from dotenv import load_dotenv

from classification.CNNClassifier import CNNClassifier
from model.Journal import Journal, Question
from flask_mongoengine import MongoEngine

from services.features_extractor import FeaturesExtractor
from services.journal_services import JournalService
from services.spotify_services import SpotifyService

SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


spotifyService = SpotifyService()
journalService = JournalService()
featuresExtractor = FeaturesExtractor()
cnnClassifier = CNNClassifier()


app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
# app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['MONGODB_SETTINGS'] = [
#     {
#         'db': 'journal',
#         'host': 'localhost',
#         'port': 27017
#     }
#

app.config.from_pyfile('config.py')
db = MongoEngine(app)
CORS(app)


@app.route('/login')
def login():
    scope = 'user-read-private,user-read-email,playlist-read-private'
    params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'scope': scope
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})
    if 'code' in request.args:
        req_body = {
            'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
            'show_dialog': True

        }
        response = requests.post(TOKEN_URL, data=req_body)
        access_token = response.json()['access_token']
        expires = response.json()['expires_in']
        expires += datetime.datetime.now().timestamp()
        return redirect(f'http://localhost:3000/callback?access_token={access_token}&expires_in={expires}')


@app.route('/songs')
def get_tracks():
    access_token = request.headers.get('Authorization')
    search_query = request.args.get('searchName')
    sp = spotipy.Spotify(auth=access_token)
    results = sp.search(q='track:' + search_query, type='track', limit=5)
    track_names = [track['name'] for track in results['tracks']['items']]
    songs = []
    for track in results['tracks']['items']:
        songs.append({'id': track['id'], 'song': track['name'], 'artist': track['artists'][0]['name'],
                      'image': track['album']['images'][0]['url']})
    return songs


@app.route('/journal', methods=['POST'])
def post_journal():
    journalreceived = request.json
    journal = Journal.objects(email=journalreceived['email']).first()
    journal.update(**journalreceived)
    journal = Journal.objects(email=journalreceived['email']).first()

    return journal.to_json()


@app.route('/journal', methods=['PUT'])
def get_journal():
    # token = request.headers.get('Authorization')
    # email, spotify_id = spotifyService.getInstance().getEmailAndSpotifyId(token)

    email = request.json['email']
    spotify_id = request.json['spotify_id']

    journal = Journal.objects(spotify_id=spotify_id, email=email).order_by('-date').first()
    if not journal:
        journalService.getInstance().createJournal(email, spotify_id)
    else:
        #get date timestamp
        date = journal.date
        #get current date timestamp
        current_date = datetime.datetime.now().timestamp()
        #compare if there has been 24 hours since the last journal entry
        if current_date - date > 100:
            journal = journalService.getInstance().createJournal(email, spotify_id)


    journal = Journal.objects(spotify_id=spotify_id, email=email, date__gt=10).order_by('-date').exclude('id').first()
    journal = json.loads(journal.to_json())
    return journal

@app.route('/history', methods=['GET'])
def get_history():
    # token = request.headers.get('Authorization')
    # email, spotify_id = spotifyService.getInstance().getEmailAndSpotifyId(token)

    email = request.json['email']
    spotify_id = request.json['spotify_id']

    journals = Journal.objects(email=email, spotify_id=spotify_id).exclude('id').all()
    journals = json.loads(journals.to_json())
    return journals

@app.route('/forwardsong', methods=['POST'])
def feed_forward_song():
    song = request.json['song']
    return spotifyService.getInstance().downloadMp3(song)

@app.route('/classify', methods=['POST'])
def classify():
    song = request.json['song']
    path = spotifyService.getInstance().downloadMp3(song)
    features = featuresExtractor.getInstance().cnnFeatures(path)
    prediction = cnnClassifier.classify(features)
    return prediction

@app.route('/user', methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization')
    userDetails = spotifyService.getInstance().getUserDetails(token)
    return userDetails



if __name__ == '__main__':
    app.run(debug=True, port=8888)
