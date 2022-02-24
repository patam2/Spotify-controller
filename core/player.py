class SpotifyPlayer:
    def __init__(self, SpotifyClass) -> None:
        self.Spotify = SpotifyClass

    def change_playback(self):
        try:
            currently_playing = self.Spotify.get_player()
            if "device" not in currently_playing:
                print("Spotify not found")
                return
            currently_playing = not currently_playing["is_playing"]
            self.Spotify.play_music(currently_playing)
            print("Paused track" if not currently_playing else "Resuming track")
        except Exception as Error:
            print(Error, 'happened')

    def skip_song(self):
        try:
            self.Spotify.skip_song()
        except Exception as Error:
            print(Error, 'happened')

    def previous_song(self):
        try:
            self.Spotify.previous_song()
        except Exception as Error:
            print(Error, 'happened')
