from classification.CNNClassifier import CNNClassifier
from services.features_extractor import FeaturesExtractor
from services.spotify_services import SpotifyService


class ClassifierService:
    _instance = None

    cnnClassifier = CNNClassifier()
    featuresExtractor = FeaturesExtractor()
    spotifyService = SpotifyService()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getInstance(self):
        return self._instance

    def classify(self, song):
        path = self.spotifyService.getInstance().downloadMp3(song)
        features = self.featuresExtractor.cnnFeatures(path)
        prediction = self.cnnClassifier.classify(features)
        return prediction


