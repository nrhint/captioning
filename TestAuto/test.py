##Nathan Hinton.
##This program will take a text fiel and then use it to generate a srt file when the user presses a key command will mark the timestamp and other information for the user

import time
import pyscreenshot as ImageGrab
import pytesseract

screenPortion = (850, 50, 1150, 200)

##Read the file
#This will become a funtion later:
file_name = "1 Ne 2.txt"
chapter = '2'
file = open(file_name, 'r').read()

#Remove the tabs in the file
file = file.replace('\t', '')

#print(file[0:100])

def convertTime(timeInSec):
    hr = int(timeInSec//(60*60))
    mn = int((timeInSec-(hr*60*60))//60)
    sec = int((timeInSec-((hr*60*60)+mn*60))//1)
    ms = str(round(timeInSec-int(timeInSec), 3))[2:]
    return "%s:%s:%s,%s"%(hr, mn, sec, ms)

def generateVerses(text):
    lst = []
    start = 0
    for occ in range(text.count('\n')):
        end = text[start:].find('\n')
        if end == 0:
            start +=1
        else:
            print(start, end)
            lst.append(text[start:end+start])
            start = end+start+1
    lst.append(text[start:])
    return lst

text = generateVerses(file)
#Merge the chapter with the heading:
text = text[text.index('Chapter %s'%chapter):]
text[0] = text[0]+text[1]
text.pop(1)

def generateSRTSimple(timeList, verses):
    """Sample SRT:
    1
    00:00:00,000 --> 00:00:05,400
    foo bar
    [blank line]"""
    text = ''
    for ind in range(0, len(timeList)):
        try:
            text += str(ind)+'\n'
            text += convertTime(timeList[ind])+' --> '+convertTime(timeList[ind+1])+'\n'
            text += str(verses[ind])+'\n'
            text += '\n'
        except IndexError:
            print("Index Error Occoured")
    open('test2.txt', 'w').write(text)
    return text

def generateSRTAdvanced(fullTimeList, verses, ccLength = 10):
    text = ''
    ccNumber = 0
    timeList = fullTimeList[0:len(verses)+1]
    for ind in range(0, len(timeList)-1):
        print("verse %s"%ind)
        #Sample the verse to generate appropriate sized chunks
        verse = verses[ind]
        start = timeList[ind]
        if start < 0:
            start = 0
#        print(start)
        end = timeList[ind+1]
        words = verse.count(' ')
        divisions = (words//ccLength)+1
        approx = round(words/divisions, 0)
        words = verse.split(' ')
        ##Generate the times for this verse
        duration = end-start
        smallDuration = duration/divisions
#        print(start, end, duration, divisions, smallDuration)
        ##Generate the lines for the file
        for div in range(0, divisions):
            tend = (div+1)*ccLength
            tstart = div*ccLength
#            print(tend)
            if div == divisions:
                captionText = words[tstart:]
            else:
                captionText = words[tstart:tend]
            #convert the caption text from a list to a string
            finalCaptionText = ''
            for w in captionText:
                finalCaptionText += str(w)+' '
            text += str(ccNumber)+'\n'
            text += convertTime(start+(smallDuration*div))+' --> '+convertTime(start+(smallDuration*(div+1)))+'\n'
#            print(div, convertTime(start+(smallDuration*div))+' --> '+convertTime(start+(smallDuration*(div+1)))+'\n')
            text += str(finalCaptionText)+'\n'
            print(finalCaptionText)
            text += '\n'
            ccNumber += 1
    open('ADV%s.srt'%file_name, 'w').write(text)
    return text
#            print(captionText)
            
        
        

#init pynput:
from pynput import keyboard

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

##Main loop to capture the stuff

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
