##
import cv2
import pytesseract
import time

from util.time_util import convertTime
#from data.Subtitle import Subtitle
from util.text_util import findFirstPrefix

header = ''
max_time = 5
min_time = 0.5

def maxSkip():
    cap.set(1, f_max)
    

def findTimer(cv2, cap, fps, frame_count, prefix):
    times = []
    for f in range(0, frame_count, int(fps * max_time)):
        cap.set(1, f)
        ret, frame = cap.read()
        tempText = ''
        if ret == True:
            foundText = pytesseract.image_to_string(frame)
            matchText = findFirstPrefix(foundText, prefix)
            if tempText != matchText:
                print(matchText + "\t" + convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
                times.append(convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))#append the timestamp    
                tempText = matchText
        
        else:
            break;

#
def readTextFromVideo(url, prefix):

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    

    cap = cv2.VideoCapture(url)
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    minutes = int(duration / 60)
    seconds = duration % 60

    print('fps = ' + str(fps) + '\tnumber of frames = ' + str(frame_count) + '\tduration (S) = ' + str(duration))
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
    # Display the resulting frame
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('frame (W:H) = ' + str(frameWidth) + ':' + str(frameHeight) + '\n')

    startProcess = time.time()#Use for speed testing
    
    times = findTimer(cv2, cap, fps, frame_count, prefix)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    endProcess = time.time()

    print('It took %s seconds to process the video'%(endProcess-startProcess))

    return times