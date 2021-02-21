from data.verse import Verse
from util.file_util import read_file
from util.text_util import is_verse, find_number, remove_number, remove_space

def new_verse_with_value(book, chapter_number, is_header, verses, text):
    prefix = '%s %s'%(book.video_prefix, chapter_number)
    verse = Verse()
    verse.number = find_number(text)
    verse.chapter = prefix
    verse.id = prefix
    verse.text = text
    if verse.number > 0:
        verse.id = '%s:%s'%(prefix, verse.number)
    elif book.scripture == 'bofm':
        verse.id += 'H'
    verses.insert(verse.number, verse)
    

def get_verse_from_file(book, chapter_number):
    file = read_file('Resources/Verse/%s/%s'%(book.scripture, book.book_name), '%s %s'%(book.video_prefix, chapter_number), 'txt')
    print('-- Reading Text from --\n\t%s %s\n'%(book.video_prefix, chapter_number))
    text_split = file.split('\n')
    verses = [] * len(text_split)

    for text in text_split:
        if is_verse(text):
            new_verse_with_value(book, chapter_number, False, verses, text)
        elif verses:
            verses[0].text += '\n' + text
        else:
            new_verse_with_value(book, chapter_number, True, verses, text)
    return verses