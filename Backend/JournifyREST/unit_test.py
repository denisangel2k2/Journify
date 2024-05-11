import unittest
from services.features_extractor import FeaturesExtractor

class UnitTestCase(unittest.TestCase):

    def setUp(self):
        self.featureExtractor = FeaturesExtractor()

    def test_extract_features(self):
        audio_path = 'test/test_song.mp3'

        features = self.featureExtractor.lstmFeatures(audio_path)

        self.assertEqual(features.shape, (3, 1, 161, 430))
        self.assertTrue((features >= 0).all())


if __name__ == '__main__':
    unittest.main()
