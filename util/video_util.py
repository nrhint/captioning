##
import cv2
import pytesseract
import time

from data.video import Video
from util.time_util import convert_time
from util.text_util import filter_by_prefix

header = ''
max_time = 8
min_time = 0.5
division = 2


def get_text_from_frame(video, f, prefix):
    video.cap.set(1, f)
    ret, frame = video.cap.read()
    text = ''
    if ret == True:
        foundText = pytesseract.image_to_string(frame)
        text = filter_by_prefix(foundText, prefix)
        #print('\t++ Found ++ \t' + foundText)
        #print('\t++ Filter ++ \t' + text)
    return text

def find_backward(video, text, previous_text, max_f, from_f, prefix):

    start_size = max_time / 2
    end_size = min_time

    while start_size >= end_size:
        last_f = max_f
        rate = int(-1 * start_size * video.fps)
        max_f = max_f+rate
        #print('\t\t\tReduce by %s second from %s to %s by %s'%(start_size, max_f, from_f, rate))
        for f in range(max_f, from_f, rate):
            new_text = get_text_from_frame(video, f, prefix)
            if new_text == text:
                max_f = f
                last_f = max_f
                #print('\t\t\t\tstill found %s at %s and new is %s'%(new_text, f, last_f))
            elif new_text == previous_text:
                #print('\t\t\t\tbreak found %s at %s and old is %s'%(new_text, f, last_f))
                break
        start_size = start_size / division
    
    #print('\t\t\tLast Time found at frame %s'%(last_f))
    return last_f

def find_forward(video, verse, from_f, to_f, increment, previous_text, next_text):
    temp = previous_text
    for f in range(from_f, to_f, increment):
        new_text = get_text_from_frame(video, f, verse.chapter)
        if verse.chapter in new_text and new_text != temp:
            temp = new_text
            max_time = convert_time(video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
            print('\t\tFirst Time found %s at frame %s and time %s'%(new_text, f, max_time))
            if new_text == verse.id:
                if verse.start_frame is None:
                
                    min_frame = find_backward(video, verse.id, previous_text, f, from_f, verse.chapter)
                
                    video.cap.set(1, min_frame)
                    video.cap.read()
                    min_time = convert_time(video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                    print('\t\tFinally Start Time found %s at frame %s and time %s'%(new_text, min_frame, min_time))
                
                    verse.start_frame = min_frame
                    verse.start_time = min_time
                #else:
                    #print('already set')
            elif verse.chapter in new_text: #== next_text or new_text ==  + ":" +str(int(verse.number)+2):

                min_frame = find_backward(video, next_text, verse.id, f, from_f, verse.chapter)
            
                video.cap.set(1, min_frame)
                video.cap.read()
                min_time = convert_time(video.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                print('\t\tFinally End Time found %s at frame %s and time %s'%(new_text, min_frame, min_time))
            
                verse.end_frame = min_frame
                verse.end_time = min_time
                break

    return verse
    
def find_time(video, verses):

    print("\n-- Finding Verse --")
    for verse_index in range(0, len(verses), 1):
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
        start_frame = 0
        end_frame = video.frame_count
        inc_rate = int(video.fps * max_time)

        if not (verse.number is None):
            start_frame = int(verse.start_frame)

        print("\n\t" + verse.id)
        print("\tFrom: %s-%s"%(start_frame,end_frame))

        # fin min/max for both rate and time for current verse
        verse = find_forward(video, verse, start_frame + inc_rate, end_frame, inc_rate, previous_text, next_text)
        
        if verse_index != len(verses) - 1:
            next_verse.start_frame = verse.end_frame
            next_verse.start_time = verse.end_time

        endProcess = time.time()
        print('\tIt took %s seconds to process the verse'%(endProcess-startProcess))
        verse.print()

#
def get_time_from_video(verses, url):

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    video = Video()
    video.cap = cv2.VideoCapture(url)
    video.findDetail()
    video.print()

    startProcess = time.time()#Use for speed testing
    
    find_time(video, verses)

    # When everything done, release the capture
    video.cap.release()
    cv2.destroyAllWindows()

    endProcess = time.time()

    print('It took %s seconds to process the video'%(endProcess-startProcess))