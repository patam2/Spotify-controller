import json
import os
from core import kboard

parentdir = os.path.join(os.path.dirname(__file__) + "/../")

#todo - write as class?
def get_settings():
    settings = {}
    if "settings.json" not in os.listdir(parentdir):
        settings["client_id"] = input(
            "Create an application @ https://developer.spotify.com/dashboard/applications and provide the following\nClient id: "
        )
        settings['client_secret'] = input('Client secret: ')
        settings['refresh_token'] = ''
        settings['keybind_pause'] = kboard.listen_for_hotkey('Press the keys (no enter) you want for the pause/play keybind THEN press ESC: ')
        settings['keybind_skip'] = kboard.listen_for_hotkey('Press the keys (no enter) you want for the skip song keybind THEN press ESC: ')
        settings['keybind_previous'] = kboard.listen_for_hotkey('Press the keys (no enter) you want for the previous song keybind THEN press ESC: \n')
        return settings

    settings = json.loads(open(f'{parentdir}/settings.json').read())
    return settings

def save_settings(settings):
    set_file = open(f'{parentdir}/settings.json', 'w')
    set_file.write(json.dumps(settings))
    set_file.close()