##
from util.time_util import convert_time
from util.text_util import remove_start_space

def generate_srt_adv(verses, ccLength = 50):
    text = ''
    ind = 1
    for verse in verses:
        tstart = 0
        tend = 0
        words = verse.text
        divisions = 1
        while len(words)/divisions > ccLength:
            divisions += 1
        ccLength = int(len(words)/divisions)#This will set the ccLength to a closer value to make it more consistent.
        #print('\n' + str(verse.number) + '\t' + verse.text)
        words = [char for char in verse.text]
        ##Generate the times for this verse
        if verse.end_frame is None or verse.start_frame is None:
            print('\t%s missing time: %s : %s'%(verse.id, verse.start_frame, verse.end_frame))
            continue
            
        duration = int(verse.end_time)-int(verse.start_time)
        smallDuration = round(duration/divisions, 3)
        #print('%s\t%s\t%s\t%s\t%s'%(verse.id, verse.start_frame, verse.end_frame, smallDuration, divisions))
        ##Generate the lines for the file
        for div in range(0, divisions):
            #print(ind)
            if tend != 0:
                tstart = tend
            tend = (div+1)*ccLength
            if tend >= len(words):
                tend = len(words)-1
            else:
                while words[tend] != ' ':
                    tend -= 1
            
            #tstart = div*ccLength
            new_start_time = verse.start_time + (smallDuration * div)
            new_end_time = verse.start_time + (smallDuration * (div + 1))
            if div == divisions - 1:
                captionText = words[tstart:]
                new_end_time = verse.end_time
            else:
                captionText = words[tstart:tend]
            #convert the caption text from a list to a string
            finalCaptionText = ''
            for w in captionText:
                finalCaptionText += str(w)
            #print("%s: %s %s"%(ind, tstart, tend))
            try:
                finalCaptionText = remove_start_space(finalCaptionText)
                #if finalCaptionText[1] == '\n':
                    #finalCaptionText = finalCaptionText[2:]
            except IndexError:
                pass
            text += str(ind)+'\n'
            text += str(convert_time(new_start_time))+' --> '+ str(convert_time(new_end_time))+'\n'
            text += str(finalCaptionText)+'\n'
            text += '\n'
            ind += 1

    return text