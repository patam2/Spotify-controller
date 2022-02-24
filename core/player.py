class SpotifyPlayer:
    def __init__(self, SpotifyClass) -> None:
        self.Spotify = SpotifyClass

    def change_playback(self):
        currently_playing = self.Spotify.get_player()
        if isinstance(currently_playing, bool):
            print("Spotify not found")
            return
        currently_playing = not currently_playing["is_playing"]
        self.Spotify.play_music(currently_playing)
        print("Paused track" if not currently_playing else "Resuming track")

    def skip_song(self):
        self.Spotify.skip_song()
        print('Skipped to next song')

    def previous_song(self):
        self.Spotify.previous_song()
        print('Skipped to previous song')