import datetime
import os
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS, cross_origin
import librosa
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib
import numpy as np
import torch
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset,DataLoader
import torch.nn as nn
import librosa
import os
import time
from tempfile import TemporaryDirectory
from torchvision import datasets, models, transforms
from sklearn.preprocessing import minmax_scale
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

def extract_features(filepath):
    y, sr = librosa.load(filepath)
    mfccs = librosa.feature.mfcc(y=y, sr=sr)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    cens = librosa.feature.chroma_cens(y=y, sr=sr)
    n_fft = 2048
    hop_length = 512
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)
    combined_features = np.concatenate([mfccs, centroid, cens, mel_spectrogram], axis=0)
    normalized_features = minmax_scale(combined_features, axis=1) 
    return normalized_features

class MyDataset(Dataset):
    def __init__(self, data, transform=None):
        self.inputs = []
        self.labels = []
        self.transform=transform
        for i in range(4):
            for filename in os.listdir(data + str(i)):
                audio_file = str(data + str(i) + "/" + filename)
                spectrogram = extract_features(audio_file)
                print(audio_file+' '+str(spectrogram.shape))
                if spectrogram is not None:  
                    self.inputs.append(spectrogram)
                    self.labels.append(i)


        self.inputs = np.stack(self.inputs)
        self.labels = np.array(self.labels)

        self.inputs = torch.tensor(self.inputs, dtype=torch.float32).unsqueeze(1)
        self.labels = torch.tensor(self.labels)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        item = self.inputs[idx]
        target = self.labels[idx]

        if self.transform:
            item = self.transform(item)

        return item, target
    
transform=transforms.Compose([
    transforms.Normalize((0.5,), (0.5,))
])
#db=MyDataset('./Research/ModelTraining/data/1200songs2_test/',transform=transform)

client = MongoClient('mongodb://localhost:27017/')
db = client['journify']
collection = db['journals']

collection.insert_one({'title': 'test', 'content': 'test', 'mood': 0})

for document in collection.find():
    print(document)
    


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


@app.route('/test')
def test_model():
    
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 4)
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=1, padding=2, bias=True)
    model.load_state_dict(torch.load('./Research/ModelTraining/models/9e4SGD_88acc.pth'))
    model.to(device)

    model.eval()
    dataloader = torch.utils.data.DataLoader(db, batch_size=1, shuffle=True)
    inp,lab=next(iter(dataloader))

    pred=model(inp.to(device))
    return jsonify({'prediction': pred.argmax(dim=1).item(), 'label': lab.item()})


if __name__ == '__main__':
    app.run(debug=True, port=8888)
