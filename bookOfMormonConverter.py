##Nathan Hinton, Brother Golf
##This will take the srt file that is found on the book of mormon disk and reformat it to look nicer

#from util import text_util
class BofMConvert:
    def __init__(self, filePath, fileName):
        self.filePath = filePath
        self.fileName = fileName
        try:
            self.fileText = open(self.filePath+filename, 'r').read()
            self.status = 'Pass'
        except FileNotFoundError:
            print("FILE NOT FOUND AT %s"%self.filePath+filename)
            self.status = 'filePath Error...'
    def run(self):
        print(self.fileText[0:100])
        self.fileText.replace('\t', ' ')
        self.fileText = self.fileText.split('\n')
        ##Parse the text:
        times = []
        text = []
        for line in self.fileText:
            if line == '':#If the line is a timestamp
                print(line)
            elif line[0] == '0':
                times.append(line)
            elif line != '\n':
                text.append(line + ' ')
            else:
                print('not captured: %s'%line)
        ##Output the new file