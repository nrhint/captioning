from data.verse import Verse
from util.text_util import is_second_intro
from util.text_util import find_number
from util.text_util import remove_number
from util.text_util import remove_space

def get_verse_from_file(book, prefix):
    file_name = 'resources/book/' + book + '/' + prefix + '.txt'
    print('-- Reading Text from --\n\t%s\n'%(file_name))
    file = open(file_name, 'r').read()
    file = remove_space(file)
    text_split = file.split('\n')
    verses = [] * len(text_split)

    for text in text_split:

        if is_second_intro(text):
            continue

        verse = Verse()
        verse_number = find_number(text)
        verse.chapter = prefix
        #print(verse_number + " : " + text)
        if verse_number.isnumeric():
            verse.id = prefix + ":" + verse_number
            v_num = int(verse_number)
            verse.number = v_num
        else:
            verse.id = prefix
            v_num = 0
        verse.text = remove_number(text)
        verses.insert(v_num, verse)
    return verses