import keyboard


def listen_for_hotkey():
    hotkstr = set()
    print('Press the keys (no enter) you want for the keybind to pause/continue THEN press ESC: ')
    for keypress in keyboard.record():
        if keypress.event_type == 'down' and keypress.name != 'esc':
            hotkstr.add(keypress.name)
        
    return '+'.join(hotkstr)

