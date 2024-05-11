from main import app
import unittest

class FlaskIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_classify_endpoint(self):
        response = self.client.post('/classify_song',
                                    json={
                                        'song': 'Complicated - Avril Lavigne'
                                    })

        self.assertEqual(response.status_code, 200)
        response = response.json
        self.assertEqual(response['prediction'], 'Happy')


if __name__ == '__main__':
    unittest.main()
