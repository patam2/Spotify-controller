import base64
import webbrowser

from core import http_sockets, threads, settings


class Spotify:
    def __init__(self):
        self.settings = settings.get_settings()
        self.client_id = self.settings['client_id']
        self.client_secret = self.settings['client_secret']
        self.refresh_token = self.settings['refresh_token']
        self.account_sess = http_sockets.SocketClient('Basic ' + base64.b64encode(str.encode('%s:%s' % (self.client_id, self.client_secret))).decode(), "accounts.spotify.com")
        if not self.refresh_token:
            self.token = self._get_refresh_token()
        else:
            self.token = self._refresh_token()['access_token']
        threads.TokenRefresher(self)
        print(self.token, self.settings, not self.client_secret)
        self.socket_sess = http_sockets.SocketClient('Bearer ' + self.token, 'api.spotify.com')
    
    def _get_refresh_token(self):
        webbrowser.open(self._get_auth_link().decode())
        code = http_sockets.CallBack()
        token_call = self._get_token(code)
        self.token = token_call['access_token'] 
        self.refresh_token = self.settings['refresh_token'] = token_call['refresh_token']
        print('here')
        settings.save_settings(self.settings)
        return token_call['refresh_token']

    # accounts.spotify.com
    def _get_auth_link(self):
        return self.account_sess.request("GET", f"/authorize?response_type=code&client_id={self.client_id}&scope=user-modify-playback-state+user-read-playback-state&redirect_uri=http://localhost:8888/callback")

    def _get_token(self, code):
        return self.account_sess.request("POST", f'/api/token?grant_type=authorization_code&code={code}&redirect_uri=http://localhost:8888/callback') 

    def _refresh_token(self):
        return self.account_sess.request("POST", f"/api/token?grant_type=refresh_token&refresh_token={self.refresh_token}")

    # api.spotify.com
    def get_player(self) -> dict:
        return self.socket_sess.request("GET", "/v1/me/player")

    def play_music(self, play: bool):
        return self.socket_sess.request(
            "PUT", "/v1/me/player/%s" % ("play" if play else "pause")
        )
