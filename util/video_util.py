##
import cv2
import pytesseract
import time

from data.video import Video
from util.time_util import convert_time
from util.text_util import filter_by_prefix

header = ''
max_time = 8
min_time = 0.25
division = 2


def get_text_from_frame(video, f, prefix):
    video.cap.set(1, f)
    ret, frame = video.cap.read()
    text = ''
    if ret == True:
        foundText = pytesseract.image_to_string(frame)
        text = filter_by_prefix(foundText, prefix)
    return text

def find_backward(video, text, previous_text, max_f, from_f, prefix):

    #print('%s -> %s'%(text, previous_text))
    start_size = max_time / division
    end_size = min_time
    last_f = max_f

    while start_size >= end_size:
        rate = int(-1 * start_size * video.fps)
        counter = 0
        max_f += rate
        from_f += rate
        #print('\t\t\tReduce by %s second from %s to %s by %s'%(start_size, max_f, from_f, rate))
        for f in range(max_f, from_f, rate):
            new_text = get_text_from_frame(video, f, prefix)
            if new_text == text:
                last_f = f
                counter = 0
                #print('\t\t\t\tstill found %s at %s and new is %s'%(new_text, f, last_f))
            elif new_text == previous_text:
                #print('\t\t\t\tbreak found %s at %s and old is %s'%(new_text, f, last_f))
                break
            if counter > 5:
                #print('\t\t\t\tbreak found %s more than 5 at %s and old is %s'%(new_text, f, last_f))
                break
            #print('\t\t\t\count %s found %s at %s and old is %s'%(counter, new_text, f, last_f))
            counter += 1
        start_size = start_size / division
        max_f = last_f
    
    #print('\t\t\tLast Time found at frame %s'%(last_f))
    return last_f

def find_forward(video, verse, from_f, to_f, increment, previous_text, next_text):
    temp = previous_text
    for f in range(from_f, to_f, increment):
        new_text = get_text_from_frame(video, f, verse.chapter)
        #max_time = video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        #print('\t\t--found %s at frame %s and time %s'%(new_text, f, max_time))
        if new_text != temp:
            temp = new_text
            if new_text == verse.id:
                if verse.start_frame is None: 
                    #max_time = video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                    #print('\t\tStart Time found %s at frame %s and time %s'%(new_text, f, max_time))
                    min_frame = find_backward(video, verse.id, previous_text, f, from_f, verse.chapter)
                    video.cap.set(1, min_frame)
                    video.cap.read()
                    min_time = video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                    #print('\t\tFinally Start Time found %s at frame %s and time %s'%(new_text, min_frame, min_time))
                
                    verse.start_frame = min_frame
                    verse.start_time = min_time
                #else:
                    #print('already set')
            elif new_text == next_text or verse.chapter in new_text: #== next_text or new_text ==  + ":" +str(int(verse.number)+2):
                #print('%s\t%s\t%s\t%s'%(next_text, new_text, new_text == next_text, verse.chapter in new_text))
                #max_time = video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                #print('\t\tEnd Time found %s at frame %s and time %s'%(new_text, f, max_time))
                min_frame = find_backward(video, next_text, verse.id, f, from_f, verse.chapter)
                video.cap.set(1, min_frame)
                video.cap.read()
                min_time = video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                #print('\t\tFinally End Time found %s at frame %s and time %s'%(new_text, min_frame, min_time))
            
                verse.end_frame = min_frame
                verse.end_time = min_time
                break
    return verse
    
def find_time(video, verses):

    print("\n-- Finding Verses in Video --")
    for verse_index in range(0, len(verses)):
        
        startProcess = time.time()#Use for speed testing
        verse = verses[verse_index]
        
        if verse_index == 0:
            previous_text = ''
        else:
            previous_verse = verses[verse_index - 1]
            previous_text = previous_verse.id

        if verse_index == len(verses) - 1:
            next_text = ''
        else:
            next_verse = verses[verse_index + 1]
            next_text = next_verse.id
        
        end_frame = video.frame_count
        inc_rate = int(video.fps * max_time)
        start_frame = inc_rate

        if verse.number > 0 and verse.start_frame is not None:
            start_frame += verse.start_frame

        #print("\n\t" + verse.id)
        #print("\tSearch from: %s-%s"%(start_frame,end_frame))
        # fin min/max for both rate and time for current verse
        verse = find_forward(video, verse, start_frame, end_frame, inc_rate, previous_text, next_text)
        
        if verse_index != len(verses) - 1:
            next_verse.start_frame = verse.end_frame
            next_verse.start_time = verse.end_time

        #verse.print()
        endProcess = time.time()
        print("\t%s\ttook %4.3f seconds"%(verse.id, endProcess-startProcess))
        #if verse.number % 5 == 0:
            #print('')

#
def get_time_from_video(verses, url):

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    video = Video()
    print(url)
    video.cap = cv2.VideoCapture(url)
    video.findDetail()
    video.print()

    startProcess = time.time()#Use for speed testing
    find_time(video, verses)
    if verses[0].start_time is None:
        verses[0].start_time = 0
    if verses[-1].end_time is None:
        verses[-1].end_time = video.duration
    # When everything done, release the capture
    video.cap.release()
    cv2.destroyAllWindows()
    endProcess = time.time()
    print('It took %s seconds to process the video'%(endProcess-startProcess))