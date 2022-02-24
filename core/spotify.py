import base64
import webbrowser

from core import http_sockets, threads, settings

#todo: error handling and get rid of old & stale websocket sessions
class Spotify:
    def __init__(self):
        # Load settings
        self.settings = settings.get_settings()
        self.client_id = self.settings["client_id"]
        self.client_secret = self.settings["client_secret"]
        self.refresh_token = self.settings["refresh_token"]

        # Create account session
        self.account_sess = http_sockets.SocketClient(
            "Basic "
            + base64.b64encode(
                str.encode("%s:%s" % (self.client_id, self.client_secret))
            ).decode(),
            "accounts.spotify.com",
        )

        # Get refresh token
        if not self.refresh_token:
            self.refresh_token = self._get_refresh_token()

        self.token = self._refresh_token()
        threads.TokenRefresher(self)

        # token sess
        self.socket_sess = http_sockets.SocketClient(
            "Bearer " + self.token, "api.spotify.com"
        )

    def _get_refresh_token(self):
        # Get the authorization code
        webbrowser.open(self._get_auth_link().decode())
        code = http_sockets.CallBack()

        # Get refresh token
        token_call = self._get_token(code)
        self.refresh_token = self.settings["refresh_token"] = token_call[
            "refresh_token"
        ]

        # Save settings
        settings.save_settings(self.settings)
        return token_call["refresh_token"]

    # accounts.spotify.com
    def _get_auth_link(self):
        return self.account_sess.request(
            "GET",
            f"/authorize?response_type=code&client_id={self.client_id}&scope=user-modify-playback-state+user-read-playback-state&redirect_uri=http://localhost:8888/callback",
        )

    def _get_token(self, code):
        return self.account_sess.request(
            "POST",
            f"/api/token?grant_type=authorization_code&code={code}&redirect_uri=http://localhost:8888/callback",
        )

    def _refresh_token(self) -> str:
        return self.account_sess.request(
            "POST",
            f"/api/token?grant_type=refresh_token&refresh_token={self.refresh_token}",
        )["access_token"]

    # api.spotify.com
    def get_player(self) -> dict:
        return self.socket_sess.request(
            "GET", 
            "/v1/me/player"
        )

    def play_music(self, play: bool):
        return self.socket_sess.request(
            "PUT", "/v1/me/player/%s" % ("play" if play else "pause")
        )
    
    def skip_song(self):
        return self.socket_sess.request(
            'POST', '/v1/me/player/next'
        )
    
    def previous_song(self):
        return self.socket_sess.request(
            'post', '/v1/me/player/previous'    
        )