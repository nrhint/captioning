## Manipulate Text Data

import re

#Remove the tabs in the file and then remove empty line
def removeSpace(text):
    text = text.replace('\t', '')
    text = re.sub('([\n]{2,})', '\n', text)
    return text

#Remove specific symbol on next line from text
def removeSymbolLine(text, symbol):
    text = re.sub("\n" + symbol, "", text)
    return text