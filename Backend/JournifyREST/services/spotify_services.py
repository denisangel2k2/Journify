import spotipy
import requests
import tempfile
from moviepy.editor import *
from pytube import YouTube
from youtube_search import YoutubeSearch

FILEPATH = 'temps'


class SpotifyService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getInstance(self):
        return self._instance

    def getEmailAndSpotifyId(self, token):
        sp = spotipy.Spotify(auth=token)
        user = sp.current_user()
        return user['email'], user['id']

    def getUserDetails(self, token):
        sp = spotipy.Spotify(auth=token)
        user = sp.me()
        filtered_user = {"country": user['country'], "display_name": user['display_name'], "email": user['email'],
                         "followers": user['followers']['total'], "id": user['id'], "images": user['images'][-1]['url'], "product": user['product']}
        return filtered_user

    def __getUrlForSong(self, song_name):
        query = song_name
        results = YoutubeSearch(query, max_results=1).to_dict()
        if results:
            video_id = f"https://www.youtube.com/watch?v={results[0]['id']}"
            duration = results[0]['duration']
            minutes, seconds = duration.split(':')
            duration = int(minutes) * 60 + int(seconds)

            url_suffix = results[0]['url_suffix']
            return video_id, duration, url_suffix
        else:
            return None

    def downloadMp3(self, song_name):
        try:
            url, duration, _ = self.__getUrlForSong(song_name)
            print(url, duration)
            yt = YouTube(url)
            #in C:\Users\denis\AppData\Local\Programs\Python\Python311\Lib\site-packages\pytube\cipher.py
            #you should change line 30 from re.compile(r"^\$*\w+\W") to re.compile(r"^\w+\W") or vice-versa if problems occur
            video_stream = yt.streams.filter(file_extension='mp4').first()

            print('video stream')
            video_content = requests.get(video_stream.url)

            print('video content')
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(video_content.content)
                temp_file_path = temp_file.name

            print(temp_file_path)
            video = VideoFileClip(temp_file_path, audio=True)

            audio = video.audio

            duration = int(yt.length)
            start_time = duration // 4
            end_time = start_time + 30
            print(duration, start_time, end_time)

            audio_segment = audio.subclip(start_time, end_time)
            base_filename = yt.title

            save_path = f'{FILEPATH}/song.mp3'
            audio_segment.write_audiofile(save_path, codec='mp3')
            return save_path
        except Exception as e:
            print(f"An error occured: {str(e)}")

    def checkToken(self, token):
        sp = spotipy.Spotify(auth=token)
        try:
            sp.current_user()
            return True
        except Exception as e:
            return False

    def getSongsStartingWith(self, token, search_query):
        sp = spotipy.Spotify(auth=token)
        results = sp.search(q='track:' + search_query, type='track', limit=3)
        songs = []
        for track in results['tracks']['items']:
            songs.append({'id': track['id'], 'song': track['name'], 'artist': track['artists'][0]['name'],
                          'image': track['album']['images'][0]['url']})

        results = sp.search(q='artist:' + search_query, type='track', limit=2)
        for track in results['tracks']['items']:
            songs.append({'id': track['id'], 'song': track['name'], 'artist': track['artists'][0]['name'],
                          'image': track['album']['images'][0]['url']})
        return songs

    def getSongRecommendations(self, token):
        sp = spotipy.Spotify(auth=token)
        recommendations = sp.recommendations(seed_genres=['pop', 'rock', 'hip-hop', 'jazz', 'classical', 'blues'], limit=3)
        songs = []
        for track in recommendations['tracks']:
            songs.append({'id': track['id'], 'song': track['name'], 'artist': track['artists'][0]['name'],
                          'image': track['album']['images'][0]['url']})
        return songs