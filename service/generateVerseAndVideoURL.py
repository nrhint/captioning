import re
import pickle

from data.book import Book
from util.file_util import write_file, read_file
from util.text_util import remove_space_delimeter
from util.web_util import read_from_website

print('\n-- Start Processing -- ')
csv = read_file('Resources', 'BookList', 'csv')
csv = remove_space_delimeter(csv, ',')
book_list = csv.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
book_list.pop(0) #The first line is a comment that says the purpuse of the file # Header

for book_csv in book_list:
    book_detail = book_csv.split(',')
    book = Book(book_detail[0], book_detail[1], book_detail[2], int(book_detail[3]), int(book_detail[4]), int(book_detail[5]))

    video_list = 'Chapter,\tLink'
    for chapter_number in range(1, book.max_chapter + 1):
        video_url = read_from_website(book, chapter_number)
        video_list += '\n%s,\t%s'%(chapter_number, video_url)
        print('\t%s:%s - HAVE BEEN PREPARED'%(book.video_prefix, chapter_number))
    
    try:
        write_file('Resources/Video URL', book.video_prefix, 'csv', video_list)
    except:
        print('Generate Video URL for %s unsuccess.'%(book.video_prefix))
    print('FINISH BOOK')
