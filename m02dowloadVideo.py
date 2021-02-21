import re
import pickle
import time

from data.book import Book
from util.download import download_video
from util.file_util import write_file, read_file, delete_file
from util.subtitle_util import generate_srt, generate_srt_adv
from util.text_util import remove_space_delimeter
from util.verse_util import get_verse_from_file
from util.video_util import get_time_from_video

print('\n-- Start Processing -- ')
csv = read_file('Resources', 'Book List', 'csv')
csv = remove_space_delimeter(csv, ',')
book_list = csv.split('\n') #The urlList file is a set of new line spaced links with the first one being a comment
book_list.pop(0) #The first line is a comment that says the purpuse of the file # Header

startProcessTotal = time.time()#Use for speed testing
for book_csv in book_list:
    book_detail = book_csv.split(',')
    book = Book(book_detail[0], book_detail[1], book_detail[2], int(book_detail[3]), int(book_detail[4]), int(book_detail[5]))

    video_csv = read_file('Resources/Video URL', book.video_prefix, 'csv')
    video_csv = remove_space_delimeter(video_csv, ',')
    video_list = video_csv.split('\n')
    
    print('\nDownload Book %s'%(book.video_prefix))
    startProcessBook = time.time()#Use for speed testing
    for chapter_number in range(1, book.max_chapter + 1):
        
        url = video_list[chapter_number].split(',')[1]
        file_path = 'Resources/Video/%s/%s'%(book.scripture, book.book_name)
        file_name = '%s %s'%(book.video_prefix, chapter_number)
        startProcess = time.time()#Use for speed testing
        download_video(url, file_path, file_name, 'mp4')
        endProcess = time.time()
        print("\t%s\ttook %4.3f seconds"%(file_name, endProcess-startProcess))
    print('FINISH BOOK')
    endProcessBook = time.time()#Use for speed testing
    print("\t%s\ttook %4.3f seconds"%(book.video_prefix, endProcessBook-startProcessBook))

endProcessTotal = time.time()#Use for speed testing
print("All took %4.3f seconds"%(endProcessTotal-startProcessTotal))