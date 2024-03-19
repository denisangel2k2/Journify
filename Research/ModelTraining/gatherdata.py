from pytube import YouTube
from youtube_search import YoutubeSearch
import requests
from pydub import AudioSegment
from moviepy.editor import *
import os
import tempfile
import pandas as pd
import time


def download_mp3(url,filepath,duration,song_name):
    # try:
        # yt = YouTube(url)
        # video_stream = yt.streams.filter(file_extension='mp4').first()
        # video_stream.download(filename='output_video.mp4')

        # video = VideoFileClip('output_video.mp4')
        # audio = video.audio

        # duration = int(yt.length)  # Duration of the video in seconds
        # start_time = duration // 4  # Start at 25% of the video's duration
        # end_time = start_time + 10  # Extract 10 seconds from the start time

        # audio_segment = audio.subclip(start_time, end_time)
        # base_filename = yt.title

        # audio_segment.write_audiofile("truncated_" + base_filename + ".mp3", codec='mp3')

        # # Explicitly close the resources
        # audio.close()
        # video.close()

        yt = YouTube(url)
        video_stream = yt.streams.filter(file_extension='mp4').first()
        
    
        video_content = requests.get(video_stream.url)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(video_content.content)
            temp_file_path = temp_file.name

        video = VideoFileClip(temp_file_path, audio=True)
        audio = video.audio

        duration = int(yt.length)  
        start_time = duration // 4  
        end_time = start_time + 30  

        audio_segment = audio.subclip(start_time, end_time)
        base_filename = yt.title

        audio_segment.write_audiofile(filepath+"/"+song_name + ".mp3", codec='mp3')
    # except Exception as e:
    #     print(f"An error occured: {str(e)}")


def getUrlForSong(song_name):
    # try:
        query = song_name
        results=YoutubeSearch(query, max_results=1).to_dict()
        if results:
            video_id = f"https://www.youtube.com/watch?v={results[0]['id']}"
            duration=results[0]['duration']
            minutes,seconds=duration.split(':')
            duration=int(minutes)*60+int(seconds)

            url_suffix=results[0]['url_suffix']
            return video_id,duration,url_suffix
        else:
            return None
    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")


#start timer




data=pd.read_csv('./data/1200_song_mapped.csv')


start_time = time.time()
current_entry=0

for i in range(len(data)):
    try:
        song_name=data.loc[i].values[1]+" "+data.loc[i].values[2]
        song_label=data.loc[i].values[-1]
        url,duration,_=getUrlForSong(song_name)
        download_mp3(url,f'./data/1200songs2/{song_label}/',duration,song_name)
        current_entry+=1
        if (current_entry%10==0):
            print(f"Elapsed time:{time.time()-start_time}")
    except Exception as ex:
        print(f"An error occurred: {str(ex)}, stopped at {current_entry}")

print(f"Time taken to download all songs is :{time.time()-start_time}")

