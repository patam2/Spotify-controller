import keyboard


def listen_for_hotkey(q):
    hotkstr = set()
    print(q)
    for keypress in keyboard.record():
        if keypress.event_type == 'down' and keypress.name != 'esc':
            hotkstr.add(keypress.name)
        
    return '+'.join(hotkstr)

