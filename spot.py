import keyboard
from core import spotify


spot = spotify.Spotify()

def change_playback():
    currently_playing = not spot.get_player()['is_playing']
    spot.play_music(currently_playing)
    print('Paused track' if not currently_playing else 'Resuming track')

print('Press', spot.settings['keybind'], 'to pause/play')

keyboard.add_hotkey(
    spot.settings['keybind'],
    change_playback,
    suppress=True
)
keyboard.wait()