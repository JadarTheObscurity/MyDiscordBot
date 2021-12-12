from spotdl.search import SpotifyClient
import spotdl.search.song_gatherer as gatherer
from spotdl.parsers import parse_query

SpotifyClient.init(
       client_id="5f573c9620494bae87890c0f08a60293",
       client_secret="212476d9b0f3472eaa762d90b19b0ba8",
       user_auth=False,
)

link = ["https://open.spotify.com/album/3vVDoPJZvuNXuyiyKRnUsV?si=bS1OCd6MRq2DJ2sFGx9j5g"]

song_list = parse_query(
            link,
            "mp3",
            True,
            False,
            "musixmatch",
            4,
        )

for song in song_list:
    print(f"{song.song_name}, {song.youtube_link}")

print(song_list[0].youtube_link)
#print(gatherer.from_spotify_url(link))
