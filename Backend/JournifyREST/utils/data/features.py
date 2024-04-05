import librosa
import numpy as np
from sklearn.preprocessing import minmax_scale

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