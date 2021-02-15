##
#from time_util import convertTime

def generate_srt(verses):
    text = ''
    for verse in verses:
        if verse.number is None:
            ind = 1
        else:
            ind = verse.number + 1
            
        text += str(ind)+'\n'
        text += verse.start_time+' --> '+verse.end_time+'\n'
        text += str(verse.text)+'\n'
        text += '\n'
    return text

def generate_str_adv(verses, ccLength = 10):
    text = ''
    ind = 1
    for verse in verses:
        words = verse.text.split(' ')
        
            
        text += str(ind)+'\n'
        text += verse.start_time+' --> '+verse.end_time+'\n'
        text += str(verse.text)+'\n'
        text += '\n'
    return text


    return text

#
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

#
def generateSRTAdvanced(fullTimeList, verses, ccLength = 10, file_name = 'lastOut'):
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
    open('%s.srt'%file_name, 'w').write(text)
    return text