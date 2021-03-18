import time

from data.book import Book
from util.download import download_video
from util.file_util import read_file
from util.text_util import remove_space_delimeter
from util.logging_util import add_to_log, save_log

log = ''
log = add_to_log(log, '\n-- Start Processing -- \n')
csv = read_file('Resources', 'Book List', 'csv')
csv = remove_space_delimeter(csv, ',')
book_list = csv.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
book_list.pop(0) #The first line is a comment that says the purpure of the file # Header

startProcessTotal = time.time()#Use for speed testing
for book_csv in book_list:
    book_detail = book_csv.split(',')
    book = Book(book_detail[0], book_detail[1], book_detail[2], int(book_detail[3]), int(book_detail[4]), int(book_detail[5]))

    video_csv = read_file('Resources/Video URL', book.video_prefix, 'csv')
    video_csv = remove_space_delimeter(video_csv, ',')
    video_list = video_csv.split('\n')
    
    log = add_to_log(log, '\nDownload Book %s\n'%(book.video_prefix))
    startProcessBook = time.time()#Use for speed testing
    for chapter_number in range(1, book.max_chapter + 1):
        
        url = video_list[chapter_number].split(',')[1]
        file_path = 'resources/video/%s/%s'%(book.scripture, book.book_name)
        file_name = '%s %s'%(book.video_prefix, chapter_number)
        startProcess = time.time()#Use for speed testing
        download_video(url, file_path, file_name, 'mp4')
        endProcess = time.time()
        log = add_to_log(log, "\t%s\ttook %4.3f seconds\n"%(file_name, endProcess-startProcess))
        save_log(log, file_name = 'videoDownload')
    log = add_to_log(log, 'FINISH BOOK')
    save_log(log, file_name = 'videoDownload')
    endProcessBook = time.time()#Use for speed testing
    log = add_to_log(log, "\t%s\ttook %4.3f seconds\n"%(book.video_prefix, endProcessBook-startProcessBook))

endProcessTotal = time.time()#Use for speed testing
log = add_to_log(log, "All took %4.3f seconds"%(endProcessTotal-startProcessTotal))
save_log(log, file_path='m02', file_name = 'videoDownload')
