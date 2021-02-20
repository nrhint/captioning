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
csv = open('Resources/Book List.csv', 'r').read()
csv = remove_space_delimeter(csv, ',')
bookList = csv.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
bookList.pop(0) #The first line is a comment that says the purpuse of the file # Header

for book_csv in bookList:
    book_detail = book_csv.split(',')
    book = Book(book_detail[0], book_detail[1], book_detail[2], int(book_detail[3]), int(book_detail[4]), int(book_detail[5]))

    print('\n%s - START'%(book.video_prefix))
    if book.scripture[0] == '#':
        print('Mark as skip')
        continue

    video_list = 'Chapter,\tLink'
    for chapter_number in range(book.start_chapter, book.end_chapter + 1):
        video_url = read_from_website(book, chapter_number)
        video_list += '\n%s,\t%s'%(chapter_number, video_url)
        print('\t%s:%s - HAVE BEEN PREPARED'%(book.video_prefix, chapter_number))
    write_file('Resources/Video URL', book.video_prefix, 'csv', video_list)
    print('FINISH BOOK')
