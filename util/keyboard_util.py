##
from pynput import keyboard

lastKeys = [0]#This is where other programs can find a key history.

def listener():
    def help():
        print("This function will start a keyboard listenr using pynput to listen to the keys that you press. It will start when you press the p key and keep logging the keys.")
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
            #time.sleep(1)