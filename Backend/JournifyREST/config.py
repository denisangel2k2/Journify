from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
CORS_HEADERS = 'Content-Type'
MONGODB_SETTINGS = {
    'db': 'journify',
    'host': 'localhost',
    'port': 27017
}
