##Nathan Hinton, Brother Golf
##This program will take a text fiel and then use it to generate a srt file when the user presses a key command will mark the timestamp and other information for the user

import time
import cv2

screenPortion = (850, 50, 1150, 200)

##Read the file
#This will become a funtion later:
file_name = "1 Ne 2.txt"
chapter = '2'
file = open(file_name, 'r').read()

#print(file[0:100])
#Remove the tabs in the file and then remove empty line
def removeSpace(file):
    file = file.replace('\t', '')
    file = file.replace('([\n]{2,})', '\n')
    return file

file = removeSpace(file)

def convertTime(timeInSec):
    hr = int(timeInSec//(60*60))
    mn = int((timeInSec-(hr*60*60))//60)
    sec = int((timeInSec-((hr*60*60)+mn*60))//1)
    ms = str(round(timeInSec-int(timeInSec), 3))[2:]
    return "%s:%s:%s,%s"%(hr, mn, sec, ms)

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
            
#####UPDATE WITH CV2######

video = cv2.VideoCapture('1 Ne 2.mp4')

##Read the frame then filter it to the size needed
##Apply filter 
