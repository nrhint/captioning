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

def generate_srt_adv(verses, ccLength = 50):
    text = ''
    ind = 1
    for verse in verses:
        tstart = 0
        tend = 0
        words = len(verse.text)
        divisions = math.ceil(words//ccLength) + 1
        if divisions == 0:
            divisions = 1
        #print('\n' + str(verse.number) + '\t' + verse.text)
        words = [char for char in verse.text]
        ##Generate the times for this verse
        if verse.end_time is None or verse.start_time is None:
            print('\t%s missing time: %s : %s'%(verse.id, verse.start_time, verse.end_time))
            continue
            
        duration = int(verse.end_time)-int(verse.start_time)
        smallDuration = round(duration/divisions, 3)
        #print('%s\t%s\t%s\t%s\t%s'%(verse.id, verse.start_time, verse.end_time, smallDuration, divisions))
        ##Generate the lines for the file
        for div in range(0, divisions):
            if tend != 0:
                tstart = tend
            tend = (div+1)*ccLength
            if tend > len(words):
                tend = len(words)
            else:
                while words[tend] != ' ':
                    tend -= 1
            #tstart = div*ccLength
            new_start_time = verse.start_time + (smallDuration * div)
            new_end_time = verse.start_time + (smallDuration * (div + 1))
            if div == divisions:# - 1:
                captionText = words[tstart:]
                new_end_time = verse.end_time
            else:
                captionText = words[tstart:tend]
            #convert the caption text from a list to a string
            finalCaptionText = ''
            for w in captionText:
                finalCaptionText += str(w)+''
            #print("%s: %s %s"%(ind, tstart, tend))
            if finalCaptionText[1] == '\n':
                finalCaptionText = finalCaptionText[2:]
            text += str(ind)+'\n'
            text += str(convert_time(new_start_time))+' --> '+ str(convert_time(new_end_time))+'\n'
            text += str(finalCaptionText)+'\n'
            text += '\n'
            ind += 1

    return text