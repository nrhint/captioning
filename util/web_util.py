import requests
from bs4 import BeautifulSoup   

def readFromWebsite(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    # {'label', 'h4', 'ol', '[document]', 'a', 'h1', 'noscript', 'span', 'header', 'ul', 'html', 'section', 'article', 'em', 'meta', 'title', 'body', 'aside', 'footer', 'div', 'form', 'nav', 'p', 'head', 'link', 'strong', 'h6', 'br', 'li', 'h3',
    #'h5', 'input', 'blockquote', 'main', 'script', 'figure'}

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
        'ul',
        'li',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name == 'p':
            
            #print("T: " + str(t.parent))
            output += '{} '.format(t)
            #print('{} '.format(t) + '\n')

    print(output)

    return output