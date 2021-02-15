class Verse:
    def __init__(self):
        self.id = None
        self.chapter = None
        self.number = None
        self.text = None
        self.start_time = None
        self.end_time = None
        self.start_frame = None
        self.end_frame = None

    def print(self):
        print('\n' + self.id + "\t" + self.chapter + "\t" + str(self.number))
        print(self.text)
        print('%s - %s'%(self.start_time, self.end_time))