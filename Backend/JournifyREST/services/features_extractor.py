import librosa
import numpy as np
import spotipy
from sklearn.preprocessing import minmax_scale
import os
import torch
from sklearn.preprocessing import StandardScaler
import joblib

os.environ['LIBROSA_CACHE_DIR'] = 'temps/librosa_cache'


class FeaturesExtractor:
    _instance = None

    scaler = joblib.load('classification/saved/scaler.pkl')
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getInstance(self):
        return self._instance

    def cnnCombinedFeatures(self, audio_path):
        y, sr = librosa.load(audio_path)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        return chroma_stft, rmse, spec_cent, spec_bw, rolloff, zcr, mfcc

    def cnnFeatures(self, audio_path):
        y, sr = librosa.load(audio_path)
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        cens = librosa.feature.chroma_cens(y=y, sr=sr)

        n_fft = 2048
        hop_length = 512
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)

        combined_features = np.concatenate([mfccs, centroid, cens, mel_spectrogram], axis=0)
        normalized_features = minmax_scale(combined_features, axis=1)

        return normalized_features

    def lstmFeatures(self, audio_path):
        spectogram = self.cnnFeatures(audio_path)
        spectogram = spectogram[:, :1290]
        spectogram = torch.tensor(spectogram)

        onethird = spectogram[:, :1290 // 3]
        twothirds = spectogram[:, 1290 // 3:1290 // 3 * 2]
        threethirds = spectogram[:, 1290 // 3 * 2:]

        combined = torch.stack([onethird, twothirds, threethirds])
        combined = combined.unsqueeze(1)
        return combined

    def spotifyFeatures(self, token, song):
        sp = spotipy.Spotify(auth=token)
        results = sp.search(q=song, limit=1)
        track_id = results['tracks']['items'][0]['id']

        features = sp.audio_features(track_id)[0]  # Get the first (and only) item from the list
        features_dict = {
            'danceability': features['danceability'],
            'energy': features['energy'],
            'key': features['key'],
            'loudness': features['loudness'],
            'speechiness': features['speechiness'],
            'acousticness': features['acousticness'],
            'instrumentalness': features['instrumentalness'],
            'liveness': features['liveness'],
            'valence': features['valence'],
            'tempo': features['tempo'],
            'time_signature': features['time_signature']
        }

        scaler = StandardScaler()
        scaler = joblib.load('classification/saved/scaler.pkl')
        features = list(features_dict.values())
        tensor = torch.tensor(features).unsqueeze(0)
        features_scaled = scaler.transform(tensor)
        features_scaled = torch.tensor(features_scaled)

        return features_scaled

