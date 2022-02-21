import keyboard, time
from core import spotify


spot = spotify.Spotify()
currently_playing = spot.get_player()
print(currently_playing)