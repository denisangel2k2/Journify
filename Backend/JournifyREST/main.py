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

from services.classifier_service import ClassifierService
from services.features_extractor import FeaturesExtractor
from services.journal_services import JournalService
from services.spotify_services import SpotifyService

SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REFRESH_TIME = 86400


AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

spotifyService = SpotifyService()
journalService = JournalService()
featuresExtractor = FeaturesExtractor()
cnnClassifier = CNNClassifier()
classifierService = ClassifierService()

app = Flask(__name__)

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
        refresh_token = response.json()['refresh_token']
        expires = response.json()['expires_in']
        expires += datetime.datetime.now().timestamp()
        return redirect(f'http://localhost:3000/callback?access_token={access_token}&expires_at={expires}&refresh_token={refresh_token}')

@app.route('/refresh_token', methods=['POST'])
def refresh_token():
    refresh_token = request.json['refresh_token']
    access_token = request.headers.get('Authorization')

    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=req_body)
    access_token = response.json()['access_token']
    expires = response.json()['expires_in']
    expires += datetime.datetime.now().timestamp()
    return jsonify({'access_token': access_token, 'expires_at': expires})

#move to service
@app.route('/songs')
def get_tracks():
    access_token = request.headers.get('Authorization')
    search_query = request.args.get('searchName')
    songs = spotifyService.getInstance().getSongsStartingWith(access_token, search_query)
    return songs


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
        # get date timestamp
        date = journal.date
        # get current date timestamp
        current_date = datetime.datetime.now().timestamp()
        # compare if there has been 24 hours since the last journal entry
        if current_date - date > REFRESH_TIME:
            #TODO: classify the songs for the current journal before creating a new journal

            journal = journalService.getInstance().createJournal(email, spotify_id)


    journal = Journal.objects(spotify_id=spotify_id, email=email, date__gt=10).order_by('-date').exclude('id').first()
    journal = json.loads(journal.to_json())
    return journal


@app.route('/history', methods=['PUT'])
def get_history():
    # token = request.headers.get('Authorization')
    # email, spotify_id = spotifyService.getInstance().getEmailAndSpotifyId(token)

    email = request.json['email']
    spotify_id = request.json['spotify_id']
    current_timestamp= datetime.datetime.now().timestamp()
    offset=(current_timestamp-REFRESH_TIME)
    journals = Journal.objects(spotify_id=spotify_id, email=email, date__lt=offset).order_by('-date').exclude('id')

    journals = json.loads(journals.to_json())
    return journals


@app.route('/classify_song', methods=['POST'])
def classify():
    song = request.json['song']
    path = spotifyService.getInstance().downloadMp3(song)
    features = featuresExtractor.getInstance().cnnFeatures(path)
    prediction = cnnClassifier.classify(features)
    return path


@app.route('/classify', methods=['POST'])
def update_question():
    print(request.json)
    email = request.json['email']
    spotify_id = request.json['spotify_id']
    question = request.json['question']
    index = question['index']

    journal = Journal.objects(email=email, spotify_id=spotify_id).order_by('-date').first()
    journal.questions[index].answer = question['answer']
    journal.questions[index].img = question['img']

    emotion = classifierService.getInstance().classify(question['answer'])
    journal.questions[index].emotion = emotion

    journal.save()
    journal = Journal.objects(email=email, spotify_id=spotify_id).order_by('-date').first()

    return journal.to_json()
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    token = request.headers.get('Authorization')
    return spotifyService.getInstance().getRecommendations(token)
@app.route('/report', methods=['POST'])
def get_report():
    email = request.json['email']
    spotify_id = request.json['spotify_id']

    emotion, maxEmotion = journalService.getInstance().getAverageEmotion(email, spotify_id)
    journal = Journal.objects(email=email, spotify_id=spotify_id).order_by('-date').first().update(set__emotion=maxEmotion)
    return emotion

@app.route('/all_report', methods=['POST'])
def get_report_all():
    email = request.json['email']
    spotify_id = request.json['spotify_id']

    emotions = journalService.getInstance().getAllEmotions(email, spotify_id)
    return emotions


@app.route('/user', methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization')
    userDetails = spotifyService.getInstance().getUserDetails(token)
    return userDetails


if __name__ == '__main__':
    app.run(debug=True, port=8888)
