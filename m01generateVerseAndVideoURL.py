import re

from data.book import Book
from util.file_util import write_file, read_file
from util.text_util import remove_space_delimeter
from util.web_util import read_from_website
from util.logging_util import add_to_log, save_log

log = ''
print('\n-- Start Processing -- ')
log = add_to_log(log, '\n-- Start Processing -- \n')
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

    book_name = book.video_prefix
    if book_name == '':
        book_name = book.book_name
    print('\nStart on Book %s'%(book_name))
    log = add_to_log(log, '\nStart on Book %s\n'%(book_name))
    missing_list += '\t%s:\t'%(book_name)
    detail_temp = ''
    video_list = 'Chapter,\tLink'
    for chapter_number in range(1, book.max_chapter + 1):
        video_url = read_from_website(book, chapter_number, manual_url)
        video_list += '\n%s,\t%s'%(chapter_number, video_url)
        if video_url == '-- Need Video URL --':
            print('\t(M)', end = '')
            log = add_to_log(log, '\t(M)')
            detail_temp += '\t%s %s'%(book_name, chapter_number)
        else:
            print('\t%s %s'%(book.video_prefix, chapter_number), end ='')
            log = add_to_log(log, '\t%s %s'%(book_name, chapter_number))
        if chapter_number % 10 == 0:
            print('')
            log = add_to_log(log, '\n')
        save_log(log, file_name = 'm01_generateVerseAndText')
    if detail_temp != '':
        missing_list += detail_temp + '\n'
    else:
        missing_list += "Pass\n" 
    save_log(missing_list, file_name = 'm01_missing')
    write_file('Resources/Video URL', book_name, 'csv', video_list)
    print('\nFinish Book')
    log = add_to_log(log, '\nFinish Book\n')
    save_log(log, file_name = 'm01_generateVerseAndText')

print(missing_list, end = '')
save_log(missing_list, file_name = 'm01_missing')
input()
