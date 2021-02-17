from data.verse import Verse
from util.file_util import read_file
from util.text_util import is_second_intro, find_number, remove_number, remove_space

def get_verse_from_file(book, chapter_number):
    file = read_file('resources/book/%s/%s'%(book.scripture, book.book_name), '%s %s'%(book.video_prefix, chapter_number), 'txt')
    print('-- Reading Text from --\n\t%s %s\n'%(book.video_prefix, chapter_number))
    text_split = file.split('\n')
    url = text_split[0]
    text_split.pop(0) # pop video link
    verses = [] * len(text_split)

    for text in text_split:
        if is_second_intro(text):
            verses[0].text += '\n' + text
            continue

        prefix = '%s %s'%(book.video_prefix, chapter_number)
        verse = Verse()
        verse.number = find_number(text)
        verse.chapter = prefix
        if verse.number > 0:
            verse.id = '%s:%s'%(prefix, verse.number)
        else:
            verse.id = prefix # + 'H'
        verse.text = remove_number(text)
        verses.insert(verse.number, verse)

    verses.insert(len(verses), url)
    return verses