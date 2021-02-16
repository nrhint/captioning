class Verse:
    def __init__(self, id = None, chapter = None, number = None, text = None, start_time = None, end_time = None, start_frame = None, end_frame = None):
        self.id = id
        self.chapter = chapter
        self.number = number
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.start_frame = start_frame
        self.end_frame = end_frame
    
    def print(self):
        print('\n' + self.id + "\t" + self.chapter + "\t" + str(self.number))
        print(self.text)
        print('%s - %s'%(self.start_time, self.end_time))