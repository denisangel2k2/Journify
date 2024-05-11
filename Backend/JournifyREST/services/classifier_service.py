from classification.CNNClassifier import CNNClassifier
from classification.LSTMClassifier import LSTMClassifier
from classification.SpotifyClassifier import SpotifyClassifier
from services.features_extractor import FeaturesExtractor
from services.spotify_services import SpotifyService


class ClassifierService:
    _instance = None

    # cnnClassifier = CNNClassifier()
    lstmClassifier = LSTMClassifier()
    featuresExtractor = FeaturesExtractor()
    spotifyClassifier = SpotifyClassifier()
    spotifyService = SpotifyService()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getInstance(self):
        return self._instance

    def classify(self, song):
        path = self.spotifyService.getInstance().downloadMp3(song)
        features = self.featuresExtractor.lstmFeatures(path)
        prediction = self.lstmClassifier.classify(features)
        return prediction

    def backup_classify(self, token, song):
        features = self.featuresExtractor.spotifyFeatures(token, song)
        prediction = self.spotifyClassifier.classify(features)
        return prediction
