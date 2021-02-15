import re

from util.text_util import *
from util.video_util import *


screenPortion = (850, 50, 1150, 200)
##Read the file
#This will become a funtion later:
prefix = "D&C 1"
#file_name = "resources/verse/" + prefix + ".txt"
chapter = '2'
#print(file_name)
#file = open(file_name, 'r').read()
#file = removeSpace(file)
#text = generateVerses(file)
#text = file.split('\n')
#Merge the chapter with the heading:
#text = text[text.index('Chapter %s'%chapter):]
#text[0] = text[0] + " " + text[1]
#text.pop(1)

#print(*text, sep = "\n")

#read file with links

urlList = open('resources/DAndC.csv', 'r').read()
urlList = urlList.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
urlList.pop(0) #The first line is a comment that says the purpuse of the file

for detail in urlList:
    details = detail.split(',')
    prefix = details[0]
    url = details[1]
    url = re.sub('[ ]', '', url)
    result = readTextFromVideo(url, prefix)
