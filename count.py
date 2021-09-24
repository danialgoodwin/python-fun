
# https://docs.python.org/3.8/library/collections.html#collections.Counter
# https://pypi.org/project/pynput/
# https://github.com/moses-palmer/pynput
#


from collections import Counter
from datetime import datetime
from pathlib import Path

from pynput import keyboard
from pynput.keyboard import Key

FILE = f'key-counts-{datetime.now().replace(microsecond=0).isoformat().replace(":", "-")}.json'

counter = Counter()

last_key = ''


def save():
    print(f'save()')
    Path(FILE).write_text(str(dict(counter)))


def on_press(key):
    print(f'key={key}')
    try:
        counter[key.char] += 1
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        counter[key] += 1
        print('special key {0} pressed'.format(key))


def on_release(key):
    global last_key
    if last_key == Key.esc and key == Key.f1:
        save()
        return False
    else:
        last_key = key


def start():
    print(f'start()')
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def main():
    print('main()')
    start()


if __name__ == '__main__':
    main()
