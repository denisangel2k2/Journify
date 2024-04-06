import datetime
import os
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib
import torch
import matplotlib.pyplot as plt

from tempfile import TemporaryDirectory
from pymongo import MongoClient



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   doggoy'
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)

# Spotify credentials
SPOTIFY_CLIENT_ID = 'ed81637e47634d6ea46bb787c23f6174'
SPOTIFY_CLIENT_SECRET = '72a7cb166df34b3cae769414bd582a11'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  # Must match the redirect URI in your Spotify Developer Dashboard

AUTH_URL='https://accounts.spotify.com/authorize'
TOKEN_URL='https://accounts.spotify.com/api/token'
API_BASE_URL='https://api.spotify.com/v1/'
# Spotipy authentication




client = MongoClient('mongodb://localhost:27017/')
db = client['journify']
collection = db['journals']



@app.route('/login')
def login():
    scope='user-read-private,user-read-email,playlist-read-private'
    params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'scope': scope
    }
    auth_url=f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

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
        expires= response.json()['expires_in']
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
        songs.append({'id': track['id'], 'song': track['name'], 'artist': track['artists'][0]['name'], 'image': track['album']['images'][0]['url']})
    return songs


if __name__ == '__main__':
    app.run(debug=True, port=8888)
