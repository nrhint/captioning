import requests
from bs4 import BeautifulSoup   
from util.file_util import write_file
from util.text_util import find_video_id
from util.text_util import format_HTML

def read_from_website(book, chapter_number):

    video_url = '-- Need Video URL --'

    url = 'https://www.churchofjesuschrist.org/study/scriptures/%s/%s/%s?lang=ase'%(book.scripture, book.book_name, chapter_number)
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    verse_text = soup.find("div", {"class": "body"})
    metas = soup.find_all("meta")

    video_text = ''
    for meta in metas:
        video_text += '{} '.format(meta)
    
    video_id = find_video_id(video_text)
    if video_id != '':
        video_url = 'https://mediasrv.churchofjesuschrist.org/media-services/GA/size/%s/1280/720'%(video_id)

    verses = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'sup',
        # there may be more elements you don't want, such as "style", etc.
    ]
    # {'label', 'h4', 'ol', '[document]', 'a', 'h1', 'noscript', 'span', 'header', 'ul', 'html', 'section', 'article', 'em', 'meta', 'title', 'body', 'aside', 'footer', 'div', 'form', 'nav', 'p', 'head', 'link', 'strong', 'h6', 'br', 'li', 'h3',
    #'h5', 'input', 'blockquote', 'main', 'script', 'figure'}


    for t in verse_text:
        if t.parent.name not in blacklist:
            verses += '{} '.format(t)

    verses = format_HTML(verses)
    write_file('Resources/Verse/%s/%s'%(book.scripture, book.book_name), '%s %s'%(book.video_prefix, chapter_number), 'txt', verses)

    return video_url
#javascript:var x=document.getElementsByTagName('sup');for(var i=0;i<x.length;i++){void(x[0].parentNode.removeChild(x[0]));}