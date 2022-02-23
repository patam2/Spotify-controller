import keyboard
from core import spotify


spot = spotify.Spotify()
currently_playing = spot.get_player()['is_playing']

def change_playback():
    global currently_playing
    currently_playing = not currently_playing
    spot.play_music(currently_playing)
    print('Paused track' if not currently_playing else 'Resuming track')

print('Press', spot.settings['keybind'], 'to pause/play')

keyboard.add_hotkey(
    spot.settings['keybind'],
    change_playback,
    suppress=True
)
keyboard.wait()