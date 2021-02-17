##
import math
from util.time_util import convert_time

def generate_srt(verses):
    text = ''
    for verse in verses:
        verse.print()
        if verse.number is None:
            ind = 1
        else:
            ind = verse.number + 1
            
        text += str(ind)+'\n'
        text += str(convert_time(verse.start_time)) + ' --> ' + str(convert_time(verse.end_time)) + '\n'
        text += str(verse.text)+'\n'
        text += '\n'
    return text

def generate_srt_adv(verses, ccLength = 10):
    text = ''
    ind = 1
    for verse in verses:
        words = verse.text.count(' ')
        divisions = math.ceil(words//ccLength) + 1
        if divisions == 0:
            divisions = 1
        #approx = round(words/divisions, 0)
        print('\n' + str(verse.number) + '\t' + verse.text)
        words = verse.text.split(' ')
        #print('word count: ' + str(len(words)))
        ##Generate the times for this verse
        duration = int(verse.end_time)-int(verse.start_time)
        smallDuration = duration/divisions
    #        print(start, end, duration, divisions, smallDuration)
        ##Generate the lines for the file
        for div in range(0, divisions):
            tend = (div+1)*ccLength
            tstart = div*ccLength
            #print(str(tstart) + '\t' + str(tend))
    #            print(tend)
            if div == divisions:
                captionText = words[tstart:]
            else:
                captionText = words[tstart:tend]
            #convert the caption text from a list to a string
            finalCaptionText = ''
            for w in captionText:
                finalCaptionText += str(w)+' '
            text += str(ind)+'\n'
            text += str(convert_time(verse.start_time+(smallDuration*div)))+' --> '+ str(convert_time(verse.start_time+(smallDuration*(div+1))))+'\n'
    #            print(div, convertTime(start+(smallDuration*div))+' --> '+convertTime(start+(smallDuration*(div+1)))+'\n')
            text += str(finalCaptionText)+'\n'
            print('\t' + finalCaptionText)
            text += '\n'
            ind += 1

    #open('output/subtitle/D&C 1Test.srt', 'w').write(text)
    return text