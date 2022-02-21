import threading
import time

def TokenRefresher(spotc):
    def cthread():
        print('Starting token refresher thread')
        while True:
            time.sleep(3559)
            spotc.token = spotc._refresh_token()['access_token']
    threading.Thread(target=cthread, daemon=True).start()