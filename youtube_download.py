from __future__ import unicode_literals
import pprint
from youtube_dl import YoutubeDL
import sys

ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
            }
        ]
    }

print(sys.argv)

audio_downloader = YoutubeDL({'format':'bestaudio'})
try:
    with YoutubeDL(ydl_opts) as ydl:
        URL = ""
        if(len(sys.argv) == 2):
            URL = sys.argv[1]
        else:
            URL = input("Enter Youtube URL ")

#        ydl.download([URL])
        pprint.pprint(ydl.extract_info(URL, download=False))
except Exception as e:
    print(e)
    print("Couldn't download url")


