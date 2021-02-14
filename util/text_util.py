## Manipulate Text Data

import re

#Remove the tabs in the file and then remove empty line
def removeSpace(text):
    text = text.replace('\t', '')
    text = re.sub('([\n]{2,})', '\n', text)
    return text

#Remove specific symbol on next line from text
def removeSymbolLine(text, symbol):
    text = re.sub(symbol, "", text)
    text = re.sub("[\n][ ]*", "", text)
    return text

def findFirstPrefix(text, prefix):
    textList = re.findall(prefix + '[:]{0,1}[\w][\d]{0,2}', text)
    return textList[0]