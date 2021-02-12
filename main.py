from util.text_util import *
from util.video_util import *


screenPortion = (850, 50, 1150, 200)
##Read the file
#This will become a funtion later:
prefix = "1 Ne 2"
file_name = prefix + ".txt"
chapter = '2'

file = open(file_name, 'r').read()
file = removeSpace(file)
#text = generateVerses(file)
text = file.split('\n')
#Merge the chapter with the heading:
text = text[text.index('Chapter %s'%chapter):]
text[0] = text[0] + " " + text[1]
text.pop(1)

#print(*text, sep = "\n")

#read csv to get url

for url in urlList:
    Subtitle = readTextFromVideo(url)
