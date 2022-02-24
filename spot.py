import keyboard
from core import spotify
from core.player import SpotifyPlayer


spot = spotify.Spotify()
player = SpotifyPlayer(spot)


print("Press", spot.settings["keybind_pause"], "to pause/play")
print("Press", spot.settings['keybind_skip'], 'to skip the song')
print("Press", spot.settings['keybind_previous'], 'play the previous song\n')


keyboard.add_hotkey(spot.settings["keybind_pause"], player.change_playback, suppress=True)
keyboard.add_hotkey(spot.settings["keybind_skip"], player.skip_song, suppress=True)
keyboard.add_hotkey(spot.settings["keybind_previous"], player.previous_song, suppress=True)
keyboard.wait()
