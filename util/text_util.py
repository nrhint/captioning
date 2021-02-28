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

def is_verse(text):
    return re.search('[\\d]{1,3}[ ]', text)

def find_number(text):
    pattern = ('^[\\d]{1,3}')
    textList = re.findall(pattern, text)
    if not textList:
        return 0
    return int(textList[0])

def remove_number(text):
    return re.sub('^[\\d]{1,3}[ ]', '', text)

def format_HTML(text):
    text = re.sub('<sup(.+?)</sup>', '', text)
    text = re.sub('<span class="verse-number">', '\\n', text)
    text = re.sub('<p class="study-intro"(.+?)>', ' ', text)
    text = re.sub('<p class="study-summary"(.+?)>', ' ', text)
    text = re.sub('<a class="scripture-ref"(.+?)>', '\\n', text)
    text = re.sub('<(.+?)>', '', text)
    text = re.sub('[ ]{2,}', ' ', text)
    text = re.sub('^[ ]', '', text)
    return text

def find_video_id(text):
    pattern = ('"https://mediasrv.churchofjesuschrist.org(.+?)"')
    textList = re.findall(pattern, text)
    if not textList:
        return ''
    return textList[0].replace("\"", "").split("/")[-1]

def remove_space_delimeter (text, delimiter):
    text = re.sub('[ \\t]{1,}' + delimiter, delimiter, text)
    text = re.sub(delimiter + '[ \\t]{1,}', delimiter, text)
    return text

def get_url_by_verse(text, verse):
    pattern = verse + '.+'
    textList = re.findall(pattern, text)
    if not textList:
        return ''
    return textList[0]

def remove_start_space(text):
    text = re.sub('^ ', '', text)
    text = re.sub('^\\n', '', text)
    return text