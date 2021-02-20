import re
import pickle

from data.book import Book
from util.file_util import write_file, read_file
from util.subtitle_util import generate_srt, generate_srt_adv
from util.text_util import remove_space_delimeter
from util.verse_util import get_verse_from_file
from util.video_util import get_time_from_video

print('\n-- Start Processing -- ')
csv = read_file('Resources', 'Book List', 'csv')
csv = remove_space_delimeter(csv, ',')
book_list = csv.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
book_list.pop(0) #The first line is a comment that says the purpuse of the file # Header

for book_csv in book_list:
    book_detail = book_csv.split(',')
    book = Book(book_detail[0], book_detail[1], book_detail[2], int(book_detail[3]), int(book_detail[4]), int(book_detail[5]))

    video_csv = read_file('Resources/Video URL', book.video_prefix, 'csv')
    video_csv = remove_space_delimeter(video_csv, ',')
    video_list = csv.split('\n')

    for chapter_number in range(book.start_chapter, book.end_chapter + 1):
        try:
            verses = get_verse_from_file(book, chapter_number)  
            get_time_from_video(verses, video_list[chapter_number])
            adv_srt = generate_srt_adv(verses)
            write_file('Output/Subtitle/%s/%s'%(book.scripture, book.book_name), '%s %s'%(book.video_prefix, chapter_number), 'srt', adv_srt)
        except:
            print('Generate srt for %s %s unsuccess.'%(book.video_prefix, chapter_number))
    print('FINISH BOOK')