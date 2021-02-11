##Nathan Hinton, Brother Golf
##This program will take a text fiel and then use it to generate a srt file when the user presses a key command will mark the timestamp and other information for the user

import numpy as np
import time
import cv2
import pytesseract

#print(file[0:100])
#Remove the tabs in the file and then remove empty line
def removeSpace(file):
    file = file.replace('\t', '')
    file = file.replace('([\n]{2,})', '\n')
    return file

def convertTime(timeInSec):
    hr = int(timeInSec//(60*60))
    mn = int((timeInSec-(hr*60*60))//60)
    sec = int((timeInSec-((hr*60*60)+mn*60))//1)
    ms = str(round(timeInSec-int(timeInSec), 3))[2:]
    return "%s:%s:%s,%s"%(hr, mn, sec, ms)

def zeroOutTimes(timeLst):
    

############## Make into not a function
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

screenPortion = (850, 50, 1150, 200)
##Read the file
#This will become a funtion later:
prefix = "1 Ne 2"
file_name = prefix + ".txt"
chapter = '2'
file = open(file_name, 'r').read()
file = removeSpace(file)
#text = generateVerses(file)
text = file.split('\n')
#Merge the chapter with the heading:
text = text[text.index('Chapter %s'%chapter):]
text[0] = text[0] + " " + text[1]
text.pop(1)

#print(*text, sep = "\n")


# Mention the installed location of Tesseract-OCR in your system 
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

start = time.time()
times = []#init with a blank list because the program will detect when the heading starts
#####UPDATE WITH CV2######
cap = cv2.VideoCapture(prefix + '.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps
        
print('fps = ' + str(fps))
print('number of frames = ' + str(frame_count))
print('duration (S) = ' + str(duration))
minutes = int(duration / 60)
seconds = duration % 60
print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
# Display the resulting frame
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('frame (W:H) = ' + str(frameWidth) + ':' + str(frameHeight))

timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
calc_timestamps = [0.0]

#cap.set(cv2.CV_CAP_PROP_FPS, 600)

startProcess = time.time()#Use for speed testing

lastText = ""

for f in range(0, frame_count, int(fps * 10)):
    '''
Ideas for improvment:
Having the captions 10 seconds apart is not that great. It would be better if
they were closer together. One option is to increase the number of frames
checked while that would work but that will take longer. Another option is to
keep going 10 seconds but then when it changes go back 5 seconds then change
by 2.5 seconds then go by 1.25 seconds then finally go by 0.625. This is 5
iterations and would be much faster than going through more frames. This would
add 5 times the frames but aldo you couls adjust the algroythm to make it so
that you are reading every 100 frames if you are careful and make sure that
you do not skip verses.
    '''

    cap.set(1, f)
#while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:

        # Convert the image to gray scale 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        # Performing OTSU threshold 
        #ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 

        # Specify structure shape and kernel size.  
        # Kernel size increases or decreases the area  
        # of the rectangle to be detected. 
        # A smaller value like (10, 10) will detect  
        # each word instead of a sentence. 
        #rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
        
        # Appplying dilation on the threshold image 
        #dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
        
        # Finding contours 
        #contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

        # Extracted text is then written into the text file 
        #for cnt in contours: 
            #x, y, w, h = cv2.boundingRect(cnt) 
            #print("x: " + str(x) + ",y: " + str(y) + ",w: " + str(w) + ",h: " + str(h))
            
            # Drawing a rectangle on copied image 
            #rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            
            # Cropping the text block for giving input to OCR 
        #cropped = frame[y:y + h, x:x + w]
        cropped = frame[50:200, 850:1150]

            # Open the file in append mode 
            #file = open("recognized.txt", "a") 
            
            # Apply OCR on the cropped image 
        newText = pytesseract.image_to_string(cropped) 
        if prefix in newText and lastText != newText:
            print(newText + "\t" + convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
            times.append(convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))#append the timestamp
                #print(calc_timestamps[-1] + 1000/fps)
            lastText = newText


    # Break the loop
    else:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

endProcess = time.time()

print('It took %s seconds to process the video'%(endProcess-startProcess))
##Take the times and turn them into the csv file:
