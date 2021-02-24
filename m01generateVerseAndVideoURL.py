import re

from data.book import Book
from util.file_util import write_file, read_file
from util.text_util import remove_space_delimeter
from util.web_util import read_from_website

print('\n-- Start Processing -- ')
csv = read_file('Resources', 'Book List', 'csv')
csv = remove_space_delimeter(csv, ',')
book_list = csv.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
book_list.pop(0) #The first line is a comment that says the purpuse of the file # Header
#book_list = [book_list[1], 'error']

manual_url = read_file('Resources/Video URL', 'Manual URL', 'csv')
manual_url = remove_space_delimeter(manual_url, ',')

missing_list = '\nMissing Link (Please fix)\n'

for book_csv in book_list:
    book_detail = book_csv.split(',')
    book = Book(book_detail[0], book_detail[1], book_detail[2], int(book_detail[3]), int(book_detail[4]), int(book_detail[5]))

    print('\nStart on Book %s'%(book.video_prefix))
    missing_list += '\t%s:'%(book.video_prefix)
    video_list = 'Chapter,\tLink'
    for chapter_number in range(1, book.max_chapter + 1):
        video_url = read_from_website(book, chapter_number, manual_url)
        video_list += '\n%s,\t%s'%(chapter_number, video_url)
        if video_url == '-- Need Video URL --':
            print('\t(M)', end = '')
            missing_list += '\t%s %s'%(book.video_prefix, chapter_number)
        else:
            print('\t%s %s'%(book.video_prefix, chapter_number), end ='')
        if chapter_number % 10 == 0:
            print('')
    
    write_file('Resources/Video URL', book.video_prefix, 'csv', video_list)
    print('\nFinish Book')
    missing_list += '\n'

if missing_list != '\nMissing Link\n':
    print(missing_list, end = '')
input()
