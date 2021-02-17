import requests
from bs4 import BeautifulSoup   
from util.file_util import write_file
from util.text_util import find_video_id
from util.text_util import format_HTML

def read_from_website(url, scripture, book, chapter):

    res = requests.get(url)
    html_page = res.content

    #res = urllib.request.urlopen(url)
    #html_page = res.read()

    soup = BeautifulSoup(html_page, 'html.parser')
    #text2 = soup.find_all(text=True)
    text = soup.find("div", {"class": "body"})
    
    video_text = ''
    metas = soup.find_all("meta")
    for meta in metas:
        video_text += '{} '.format(meta)
    
    video_id = find_video_id(video_text)
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

    for t in text:
        if t.parent.name not in blacklist:
            verses += '{} '.format(t)

    verses = format_HTML(verses)
    
    output = '%s\n%s'%(video_url, verses)

    write_file('resources/book/%s'%(book), chapter)

    try:
        open('resources/book/%s/%s.txt'%(book, chapter), 'w').write(output)
    except FileNotFoundError:
        import os
        os.mkdir('resources/book/%s'%book)
        open('resources/book/%s/%s.txt'%(book, chapter), 'w').write(output)
    return output

    #javascript:var x=document.getElementsByTagName('sup');for(var i=0;i<x.length;i++){void(x[0].parentNode.removeChild(x[0]));}