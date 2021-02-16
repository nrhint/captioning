##Nathan Hinton This is used for testing the subtitler

#Using pickle to load a stored version of the verses data ###DO NOT USE PICKLE TO OPEN FILES THAT YOU DID NOT CREATE!###
import pickle
import math

##These will be passed to the function:

verses = pickle.load(open('test/verses.p', 'rb'))
ccLength = 10

##Function will start here
text = ''
ind = 1
for verse in verses:
    words = verse.text.count(' ')
    divisions = math.ceiling(words//ccLength)
    approx = round(words/divisions, 0)
    print(verse.text)
    words = verse.text.split(' ')
    ##Generate the times for this verse
    duration = int(verse.end_time)-int(verse.start_time)
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

        
    text += str(ind)+'\n'
    text += verse.start_time+' --> '+verse.end_time+'\n'
    text += str(verse.text)+'\n'
    text += '\n'