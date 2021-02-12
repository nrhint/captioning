import time
import pyscreenshot as ImageGrab
import pytesseract

from util.subtitle_util.py import *
from util.keyboard_util.py import *

screenPortion = (800, 50, 1150, 150)

##Read the file
#This will become a funtion later:
file_name = "1 Ne 11.txt"
chapter = '11'

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

currIm = ImageGrab.grab(screenPortion)
lastText = pytesseract.image_to_string(currIm)
print(lastText)
start = time.time()
times = [time.time()]
while run == True:
    tmpTime = time.time()
    newText = pytesseract.image_to_string(ImageGrab.grab(screenPortion))
    if lastText != newText:
        #tmpTime = time.time() #Moved to before the image is processed
        if newText == pytesseract.image_to_string(ImageGrab.grab(screenPortion)):
            if newText[0:5] == file_name[0:5]:
                times.append(tmpTime)
                lastText = str(newText)
                print(lastText)
            else:
                run = False
                print("Auto Ended...")
                times.append(time.time())
    elif lastKeys[-1] == 'e':
        times.append(time.time())
        run = False
listener.stop()
print(times)

for ind in range(len(times)):
    times[ind] = round(times[ind]-start, 3)

#times = [0.0, 2.333, 20.719, 28.77, 34.017, 46.253, 54.09, 60.25, 65.488, 69.717, 81.406, 88.491, 94.336, 106.833, 115.172, 121.591, 133.87, 142.349, 146.437, 166.14, 172.166, 182.509, 185.932, 195.028]

times2 = []
mi = int(input("Length in min "))
sec = int(input("Length in sec "))
totalTime = mi*60+sec
mult = totalTime/times[-1]
for t in times:
    times2.append((t*mult))#-(mult*0.25))#Old = 0.75, mult is the speed muluplier if watching it at a faster speed. the -3 is for the reaction time it takes to see the time change
times2[0] = 0.0
generateSRTSimple(times2, text)

generateSRTAdvanced(times2, text)

####write the file:
##
##file_name = "1Nephi10.txt"
##file = open(file_name, 'w')
##text = input("Paste the input for the chapter here:\n")
##file.write(text)
##file.close()
##