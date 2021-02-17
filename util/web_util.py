import requests
from bs4 import BeautifulSoup   
from util.text_util import format_HTML

def read_from_website(url, book, chapter):

    output = ''
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

    res = requests.get(url)
    html_page = res.content

    #res = urllib.request.urlopen(url)
    #html_page = res.read()

    soup = BeautifulSoup(html_page, 'html.parser')
    #text = soup.find_all(text=True)
    text = soup.find("div", {"class": "body"})
    
    iframes = soup.find('iframe')
    print(iframes)

    #print(text)

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    output = format_HTML(output)
    try:
        open('resources/book/%s/%s.txt'%(book, chapter), 'w').write(output)
    except FileNotFoundError:
        import os
        os.mkdir('resources/book/%s'%book)
        open('resources/book/%s/%s.txt'%(book, chapter), 'w').write(output)
    return output

    #javascript:var x=document.getElementsByTagName('sup');for(var i=0;i<x.length;i++){void(x[0].parentNode.removeChild(x[0]));}