import json
import os
from core import kboard

parentdir = os.path.join(os.path.dirname(__file__) + "/../")

#todo - write class?
def get_settings():
    settings = {}
    if "settings.json" not in os.listdir(parentdir):
        settings["client_id"] = input(
            "Create an application @ https://developer.spotify.com/dashboard/applications and provide the following\nClient id: "
        )
        settings['client_secret'] = input('Client secret: ')
        settings['refresh_token'] = ''
        settings['keybind'] = kboard.listen_for_hotkey()
        return settings
    else: #settings found
        settings = json.loads(open(f'{parentdir}/settings.json').read())
        return settings

def save_settings(settings):
    set_file = open(f'{parentdir}/settings.json', 'w')
    set_file.write(json.dumps(settings))
    set_file.close()