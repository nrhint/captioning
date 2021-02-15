## Manipulate Text Data

import re

#Remove the tabs in the file and then remove empty line
def remove_space(text):
    text = text.replace('\t', '')
    text = re.sub('([\n]{2,})', '\n', text)
    return text

def filter_by_prefix(text, prefix):
    pattern = prefix + '[:]{0,1}[\\w|\\d]{0,3}'
    textList = re.findall(pattern, text)
    if not textList:
        return ''
    return textList[0]

def find_match(text, word):
    textList = re.findall(word, text)
    if not textList:
        return ''
    return textList[0]

def is_second_intro(text):
    return re.search('^[\\d][-][\\d]', text)

def find_number(text):
    pattern = ('^[\\d]{1,2}')
    textList = re.findall(pattern, text)
    if not textList:
        return ''
    return textList[0]

def remove_number(text):
    return re.sub('^[\\d]{1,2}[ ]', '', text)