import keyboard
from core import spotify


spot = spotify.Spotify()


def change_playback():
    try:
        currently_playing = spot.get_player()
        if "device" not in currently_playing:
            print("Spotify not found")
            return
        currently_playing = not currently_playing["is_playing"]
        spot.play_music(currently_playing)
        print("Paused track" if not currently_playing else "Resuming track")
    except Exception as Error:
        print(Error, 'happened')

def skip_song():
    try:
        spot.skip_song()
    except Exception as Error:
        print(Error, 'happened')


print("Press", spot.settings["keybind_pause"], "to pause/play")
print("Press", spot.settings['keybind_skip'], 'to skip the song')

keyboard.add_hotkey(spot.settings["keybind_pause"], change_playback, suppress=True)
keyboard.wait()
