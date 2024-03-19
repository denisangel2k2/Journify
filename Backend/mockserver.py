import datetime
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   doggoy'
app.config['CORS_HEADERS'] = 'Content-Type'
# add http://localhost:3000 to cors origins
# CORS(app, origins=["http://localhost:3000"],resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app)

# Spotify credentials
SPOTIFY_CLIENT_ID = 'ed81637e47634d6ea46bb787c23f6174'
SPOTIFY_CLIENT_SECRET = '72a7cb166df34b3cae769414bd582a11'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  # Must match the redirect URI in your Spotify Developer Dashboard

AUTH_URL='https://accounts.spotify.com/authorize'
TOKEN_URL='https://accounts.spotify.com/api/token'
API_BASE_URL='https://api.spotify.com/v1/'
# Spotipy authentication

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
    

@app.route('/playlists')
def get_playlists():
    access_token = request.headers.get('Authorization')
    sp = spotipy.Spotify(auth=access_token)
    playlists = sp.current_user_playlists()
    #get top song name and danceability for each song in the playlist
    results = []
    for playlist in playlists['items']:
        print(playlist['name'])
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        playlist_tracks = sp.playlist_tracks(playlist_id)
        tracks = []
        for track in playlist_tracks['items']:
            track_id = track['track']['id']
            track_name = track['track']['name']
            track_features = sp.audio_features(track_id)
            if track_features:
                danceability = track_features[0]['danceability']
                tracks.append({'id': track_id, 'name': track_name, 'danceability': danceability})
                break
        results.append({'id': playlist_id, 'name': playlist_name, 'tracks': tracks})

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, port=8888)
