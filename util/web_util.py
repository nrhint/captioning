import requests
from bs4 import BeautifulSoup   
from util.file_util import write_file
from util.text_util import find_video_id, format_HTML, get_url_by_verse, remove_space_delimeter

def read_from_website(book, chapter_number, manual_url):

    video_url = '-- Need Video URL --'

    url = 'https://www.churchofjesuschrist.org/study/scriptures/%s/%s/%s?lang=ase'%(book.scripture, book.book_name, chapter_number)
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    verse_text = soup.find("div", {"class": "body"})
    metas = soup.find_all("meta")
    verse_name = '%s %s'%(book.video_prefix, chapter_number)

    video_text = ''
    for meta in metas:
        video_text += '{} '.format(meta)
    
    video_id = find_video_id(video_text)
    

    if video_id == '':
        new_id = get_url_by_verse(manual_url, verse_name)
        if new_id != '':
            new_id = new_id.split(',')[1]
            video_url = 'https://mediasrv.churchofjesuschrist.org/media-services/GA/size/%s/1280/720'%(new_id)
    elif verse_name == '1 Ne 5':
        video_url = 'https://mediasrv.churchofjesuschrist.org/media-services/GA/size/%s/640/360'%(video_id)
    else:
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
    write_file('Resources/Verse/%s/%s'%(book.scripture, book.book_name), verse_name, 'txt', verses)

    return video_url
#javascript:var x=document.getElementsByTagName('sup');for(var i=0;i<x.length;i++){void(x[0].parentNode.removeChild(x[0]));}