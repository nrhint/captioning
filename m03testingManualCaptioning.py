##Nathan Hinton

from pynput import keyboard
from util.time_util import convert_time
from util.file_util import write_file
from time import time, sleep

pressed = ''
def on_press(key):
    global pressed
    try:
        pressed = key.char
    except AttributeError:
        pass

def on_release(key):
    global pressed
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

while state != False:
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

When someone starts to talk press the t key. This will make the program print the line
of text that it is captioning. When the speaker has finished the pronted line release
the 't' key and wait for the next line to start t be spoken. The program will record
the start and end of when you press and release the 't' key. When the video is finished
playing then press the 'e' key to end the program.""")
        state = 'waitForGo'
    elif state == 'waitForGo':
        if pressed == 'g':
            lineIndex = 0
            baseTime = time()
            state = 'wait'
    elif state == 'wait':
        if pressed == 't':
            state = 'listen'
#        elif pressed == '':
#            state = 'released'
        elif pressed == 'e':
            state = 'end'
            print(state)
    elif state == 'listen':
        try:
            line = text[lineIndex]
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
            timeEnd = time()
            data.append([timeStart, timeEnd, line])
            lineIndex += 1
            state = 'wait'
        except IndexError:
            state = 'whoops'
    elif state == 'end':
        print("Ending...")
        state = False
    elif state == 'whoops':
        print("""
        AAH! You seem to have run out of lines. If you accidently pressed the
        't key onw too many times simply press the e key. If your video is
        still going and you have more text to caption please check the format
        of the text file with your captions. Remember that every time there is
        an enter in that file you get to press the 't' key once. This message
        was caused by there not being enough lines in the file to complete the
        action you requested.""")
        print('\nY/n continue and generate the captions with the data that I have?')
        i = input()
        if i.lower() == 'y':
            print("Okay! will do!")
            state = 'end'
        elif i.lower() == 'n':
            print("Okay. this program will now restart and wait until you give it instructions.")
            state = 'init'
        else:
            print("Invalid option... repeating instructions.")
    else:
        print("STATE ERROR")
        print("State = %s"%state)
        print("Restarting program this was caused by an internal error...")
        state = 'init'

srt = ''
number = 0
for l in data:
    srt += '%s\n'%number
    srt += '%s --> %s\n'%(convert_time(l[0]), convert_time(l[1]))
    srt += '%s\n'%l[2]
    srt += '\n'
    number += 1

try:
    write_file('output', 'captions', 'srt', srt)
except:
    print('Generate test unsuccess.')
print('File saved in %s/%s.%s'%('output', 'captions', 'srt'))
print(data)
