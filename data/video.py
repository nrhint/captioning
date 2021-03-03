import cv2
from util.logging_util import add_to_log

class Video:
    def __init__(self):
        self.cap = None
        self.fps = None
        self.frame_count = None
        self.duration = None
        self.width = None
        self.height = None

    def print(self, log = None):
        print('-- Video Detail --')
        print('\tFPS:\t%.3f'%(self.fps))
        print('\tFrames:\t%s'%(self.frame_count))
        print('\tDuration (s):\t%.3f'%(self.duration))
        print('\tDuration (m:s):\t%s : %.3f'%(int(self.duration/60),self.duration%60))
        print('\tframe (W:H):\t%s : %s'%(self.width,self.height))
        if log != None:
            return add_to_log(log, '-- Video Detail --\n\tFPS:\t%.3f\n\tFrames:\t%s\n\tDuration (s):\t%.3f\n\tframe (W:H):\t%s : %s'%(self.fps, self.frame_count, self.duration, self.width, self.height))

    def findDetail(self):
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count / self.fps
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    