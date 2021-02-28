##
import cv2
import numpy as np
import time

from data.video import Video
from util.time_util import convert_time

header = ''
max_time = 8
min_time = 0.25
division = 2


def get_pixel_positions(video, f, thresh):
    video.cap.set(1, f)
    ret, frame = video.cap.read()
    cv2.imwrite('tmp.jpg', frame)

    positions = []
    if ret == True:
        for row in range(50, 200):
            for col in range(850, 1150):
                if sum(frame[row][col]) > thresh*3:
                    positions.append((row, col))
    return positions

def calculate_prob(previous_pixels, current_pixels, sensitivity = 5):
    differences = np.setdiff1d(previous_pixels, current_pixels)
    if len(differences) > sensitivity:
        print("Different")
        return True
    else:
        print("Same")
        return False

def find_backward(video, last_positions, max_frame, thresh):
    curr_f = max_frame
    start_size = max_time/division
    rate = int(-1 * start_size * video.fps)
    while start_size >= min_time:
        if calculate_prob(last_positions, get_pixel_positions(video, curr_f-rate, thresh)):
            curr_f += rate
        else:
            curr_f -= rate
                
        start_size = start_size/division
        rate = int(-1 * start_size * video.fps)
        print(rate, curr_f)
    return curr_f



def find_forward(video, verse, start_frame, end_frame, inc_rate, last_positions, thresh):
    f = start_frame
    new_positions = get_pixel_positions(video, f, thresh)
    while not calculate_prob(last_positions, new_positions):
        f += inc_rate
        new_positions = get_pixel_positions(video, f, thresh)
    end_frame = find_backward(video, last_positions, f, thresh)
    verse.start_frame = start_frame
    verse.end_frame = end_frame
    verse.start_time = convert_time(start_frame)
    verse.end_time = convert_time(end_frame)
    return verse
   
def find_times(video, verses, thresh = 150):

    print("\n-- Finding Verses in Video --")
    positions = get_pixel_positions(video, 100, thresh)
    for verse_index in range(0, len(verses)):
        
        startProcess = time.time()#Use for speed testing
        verse = verses[verse_index]
        
        if verse_index == len(verses) - 1:
          pass
        else:
            next_verse = verses[verse_index + 1]
        end_frame = video.frame_count
        inc_rate = int(video.fps * max_time)
        start_frame = inc_rate

        if verse.number > 0 and verse.start_frame is not None:
            start_frame += verse.start_frame

        print("\n\t" + verse.id)
        print("\tSearch from: %s-%s"%(start_frame,end_frame))
        # fin min/max for both rate and time for current verse
        verse = find_forward(video, verse, start_frame, end_frame, inc_rate, positions, thresh)
        
        if verse_index != len(verses) - 1:
            next_verse.start_frame = verse.end_frame
            positions = get_pixel_positions(video, verse.end_frame, thresh)
            next_verse.start_time = verse.end_time
        if verse_index == 0:
            verse.start_frame = 0

        #verse.print()
        endProcess = time.time()
        print("\t%s\ttook %4.3f seconds"%(verse.id, endProcess-startProcess))
        #if verse.number % 5 == 0:
    return verse

#
def get_time_from_video(verses, url):

    video = Video()
    print(url)
    video.cap = cv2.VideoCapture(url)
    video.findDetail()
    video.print()

    calculate_prob(get_pixel_positions(video, 100, 200), get_pixel_positions(video, 101, 200))

    startProcess = time.time()#Use for speed testing
    find_times(video, verses)
    if verses[0].start_time is None:
        verses[0].start_time = 0
    if verses[-1].end_time is None:
        verses[-1].end_time = video.duration
    # When everything done, release the capture
    video.cap.release()
    cv2.destroyAllWindows()
    endProcess = time.time()
    print('It took %s seconds to process the video'%(endProcess-startProcess))