##
from pynput import keyboard

def listener:
    lastKeys = [0]
    def on_press(key):
        try:
            lastKeys.append(key.char)
        except AttributeError:
            pass

    def on_release(key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    wait = True
    while wait == True:
        if lastKeys[-1] == 'p':
            print("HAHAHAHAHAHA")
            wait = False
            run = True
            time.sleep(1)