##Nathan Hinton

from pynput import keyboard
from util.time_util import convert_time
from time import time, sleep

pressed = ''
def on_press(key):
    try:
        pressed = key.char
        print(pressed)
    except AttributeError:
        pass

def on_release(key):
    pressed = ''
    if key == keyboard.Key.esc:
        # Stop listener
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

##Print out the instructions:
print("Welcome to the manual captioning!")
print("This will take a text file that you have generated and it will turn it into captions!")

state = 'init'

while state != 'end':
    if state == 'init':
        i = input('What is the file path of the text file? ')
        try:
            text = open(i, 'r').read()
            state = 'parse'
        except FileNotFoundError:
            print("File not found. Please try again...")
            print()
        data = []
    elif state == 'parse':
        text = text.split('\n')
        print("""
The file is ready, to use this program please read the instructions then press the 'g' key.

When someone starts to talk press the t key. This will make the program pring the line
of text that it is captioning. When the speaker has finished the pronted line release
the 't' key and wait for the next line to start t be spoken. The program will record
the start and end of when you press and release the 't' key. When the video is finished
playing then press the 'e' key to end the program.""")
        state = 'wait'
    elif state == 'wait':
        if pressed == 'g':
            state = 'listen'
        elif pressed == 't':
            state = 'pressed'
        elif pressed == '':
            state = 'released'
        elif pressed == 'e':
            state = 'end'
    elif state == 'listen':
        for line in text:
            print('You are captioning: %s'%line)
            wait = True
            p = False
            while wait:
                if pressed == 't':
                    timeStart = time()
                    p = True
                elif pressed != 't' and p:
                    timeEnd = time()
                    wait = False
                print(pressed)
            timeEnd = time()
            data.append([timeStart, timeEnd, line])

open('test/test.srt', 'w').write(data)
print(data)
