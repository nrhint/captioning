import re
import pickle

from data.book import Book
from util.file_util import write_file
from util.subtitle_util import generate_srt, generate_srt_adv
from util.text_util import remove_space_delimeter
from util.verse_util import get_verse_from_file
from util.video_util import get_time_from_video
from util.web_util import read_from_website

print('\n-- Start Processing -- ')
csv = open('resources/book/capture.csv', 'r').read()
csv = remove_space_delimeter(csv, ',')
bookList = csv.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
bookList.pop(0) #The first line is a comment that says the purpuse of the file # Header

mode = input("\n\t- 'p' for only prepare source from web\n\t- 's' for generate subtitle'\n\t- 'a' for do everything\n\t\tEnter the mode you want: ")

need_fix_book = []

for book_csv in bookList:
    book_detail = book_csv.split(',')
    book = Book(book_detail[0], book_detail[1], book_detail[2], int(book_detail[3]), int(book_detail[4], int(book_detail[5])))

    print('\n%s - START'%(book.video_prefix))
    if book.scripture[0] == '#':
        print('Mark as skip')
        continue

    if mode == 'p' or mode == 'P' or mode == 'a' or mode == 'A':
        for chapter_number in range(book.start_chapter, book.end_chapter + 1):
            need_fix = read_from_website(book, chapter_number)
            if need_fix:
                need_fix_book.insert(len(need_fix_book), need_fix)
            print('\t%s:%s - HAVE BEEN PREPARED'%(book.video_prefix, chapter_number))

    if mode == 's' or mode == 'S' or mode == 'a' or mode == 'A':
        for chapter_number in range(1, book.max_chapter + 1):
            verses = get_verse_from_file(book, chapter_number)  
            get_time_from_video(verses)
            #pickle.dump(verses, open('test/verses.p', 'wb'))
            #srt = generate_srt(verses)
            #open('output/book/%s/test_%s.srt'%(book, prefix), 'w').write(srt)
            adv_srt = generate_srt_adv(verses)
            write_file('output/book/%s/%s'%(book.scripture, book.book_name), '%s %s'%(book.video_prefix, chapter_number), 'srt', adv_srt)
            #print('SRT file for %s written at %s'%(prefix, 'output/book/%s/%s.srt'%(book, prefix)))
    
    print('FINISH BOOK')

print('\n-- Done Processing -- ')
if need_fix_book:
    print('Need to fix')
    for need_fix in need_fix_book:
        for name in need_fix:
            print('\t%s'%name)
