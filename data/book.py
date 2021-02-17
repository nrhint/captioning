class Book:
    def __init__(self, scripture = None, book_name = None, video_prefix = None, max_chapter = 1, start_chapter = 1, end_chapter = 1):
        self.scripture = scripture
        self.book_name = book_name
        self.video_prefix = video_prefix
        self.max_chapter = max_chapter
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter
