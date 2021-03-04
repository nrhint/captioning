##
import cv2
import time

from data.video import Video
from util.time_util import convert_time
from util.logging_util import save_log, add_to_log

header = ''
max_time = 8
min_time = 0.25
division = 2

def save_frame(name, frame):
    cv2.imwrite('%s.jpg'%name, frame)

def get_pixel_positions(video, f, thresh, name = 'tmp'):
    video.cap.set(1, f)
    ret, frame = video.cap.read()
    #save_frame(name, frame)
    #frame = frame[50:200, 850:1150]
    positions = []
    if ret == True:
        for row in range(50, 200):
            for col in range(850, 1150):
                if sum(frame[row][col]) > thresh*3:
                    positions.append((row, col))
    return positions

def calabrate_thresh(video, thresh = 100):
    video.cap.set(1, int(video.cap.get(cv2.CAP_PROP_FRAME_COUNT))-600)
    ret, frame = video.cap.read()
    save_frame('lastThreshFrame', frame[50:200, 850:1150])
    finished = False
    while finished == False:
        thresh += 1
        positions = []
        for row in range(50, 200):
            for col in range(850, 1150):
                if sum(frame[row][col]) > thresh*3:
                    positions.append((row, col))
        if len(positions)> 500:
            finished = True
    return thresh + 10

def calculate_prob(previous_pixels, current_pixels, sensitivity = 5):#Sens = 5 for BofM
    differences = abs(len(previous_pixels)-len(current_pixels))
    if differences > sensitivity:# and len(differences) <100:
        # print("Different")
        return True, differences
    else:
        # print("Same")
        return False, differences

def find_backward(video, last_positions, max_frame, thresh):
    curr_f = max_frame
    start_size = max_time/division
    rate = int(-1 * start_size * video.fps)
    while start_size >= min_time:
        calc = calculate_prob(last_positions, get_pixel_positions(video, curr_f-rate, thresh))
        if calc[0]:
            curr_f += rate
        else:
            curr_f -= rate
                
        start_size = start_size/division
        rate = int(-1 * start_size * video.fps)
        # print(rate, curr_f)
    return curr_f

def find_forward(video, verse, start_frame, end_frame, inc_rate, last_positions, thresh):
    f = start_frame+200
    new_positions = get_pixel_positions(video, f, thresh)
    prob = calculate_prob(last_positions, new_positions)
    while not prob[0]:
        f += inc_rate
        new_positions = get_pixel_positions(video, f, thresh)
        prob = calculate_prob(last_positions, new_positions)
    end_frame = find_backward(video, last_positions, f, thresh)
    verse.start_frame = start_frame
    verse.end_frame = end_frame
    verse.start_time = start_frame/video.fps
    verse.end_time = end_frame/video.fps
    return verse
   
def find_times(video, verses, log, thresh = 200):#Thresh = 150 for BofM

    print("\n-- Finding Verses in Video --")
    log = add_to_log(log, "\n-- Finding Verses in Video --")
    for verse_index in range(0, len(verses)):
        
        startProcess = time.time()#Use for speed testing
        verse = verses[verse_index]
        
        if verse_index == len(verses) - 1:
          pass
        else:
            next_verse = verses[verse_index + 1]
        end_frame = video.frame_count
        inc_rate = int(video.fps * max_time)
        if verse_index == 0:
            start_frame = 0
            positions = get_pixel_positions(video, start_frame+200, thresh, 'start')
        else:
            start_frame = verse.start_frame
 
        # if verse.number > 0 and verse.start_frame is not None:
        #     start_frame += verse.start_frame

        print("\n\t" + verse.id)
        print("\tSearch from: %s-%s"%(start_frame,end_frame))
        log = add_to_log(log, "\n\t%s\n\tSearch from: %s-%s"%(verse.id, start_frame,end_frame))
        # fin min/max for both rate and time for current verse
        verse = find_forward(video, verse, start_frame, end_frame, inc_rate, positions, thresh)
        
        if verse_index != len(verses) - 1:
            next_verse.start_frame = verse.end_frame
            positions = get_pixel_positions(video, verse.end_frame+100, thresh, 'start2')
            next_verse.start_time = verse.end_time
        if verse_index == 0:
            verse.start_frame = 0

        #verse.print()
        endProcess = time.time()
        print("\t%s\ttook %4.3f seconds"%(verse.id, endProcess-startProcess))
        log = add_to_log(log, "\t%s\ttook %4.3f seconds"%(verse.id, endProcess-startProcess))
        #if verse.number % 5 == 0:
    return log
#
def get_time_from_video(verses, url):

    log = ''
    video = Video()
    print(url)
    log = add_to_log(log, url)
    video.cap = cv2.VideoCapture(url)
    video.findDetail()
    log = video.print(log = log)

    #calculate_prob(get_pixel_positions(video, 100, 200), get_pixel_positions(video, 101, 200))

    startProcess = time.time()#Use for speed testing
    thresh = calabrate_thresh(video)
    print('threshold for this video is %s'%thresh)
    log = add_to_log(log, 'threshold for this video is: %s'%thresh)
    # if 'D&C' not in verses[0].chapter:
    #     print("Not D&C")
    #     log = find_times(video, verses, log, thresh = 150)
    # else:
    #     print("D&C")
    #     
    log = find_times(video, verses, log, thresh)
    if verses[0].start_time is None:
        verses[0].start_time = 0
    if verses[-1].end_time is None:
        verses[-1].end_time = video.duration
    # When everything done, release the capture
    video.cap.release()
    cv2.destroyAllWindows()
    endProcess = time.time()
    print('It took %s seconds to process the video'%(endProcess-startProcess))
    log = add_to_log(log, 'It took %s seconds to process the video'%(endProcess-startProcess))
    save_log(log, file_name = 'video_util_m2_log'+verses[0].chapter)