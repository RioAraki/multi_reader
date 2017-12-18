import requests
import re
from bs4 import BeautifulSoup

# in some page a decode is needed for correct chinese display
def convert_zh(string):
    return string.encode('latin1').decode('gb2312')


# address -> the url of novel's index
def parse_index_kanunu(soup, book_idx, url):
    all_chapter = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and book_idx in href:
            if book_idx in url:
                print (url)
                print (book_idx)
                pos = url.index(book_idx)
                print (pos)
                abs_link = url[:pos] + href
                all_chapter.append(abs_link)
            else:
                print('Cannot find book index')
                return False

    print(all_chapter)
    return all_chapter


def parse_index_ty2016(address):
    all_chapter = []
    page = requests.get(address)

# # convert the link to absolute link
# def link_convert_kanunu(link, url, book_idx):
#


# def md():

#
def route(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # parse the link, find out which site does it comes from
    site = ''
    if 'kanunu' in url:
        site = 'kanunu'
        book_idx = re.search('([0-9]+).$', url)
        parse_index_kanunu(soup, book_idx, url)
    elif 'ty2016' in url:
        site = 'ty2016'
    elif '99lib' in url:
        site = '99lib'
    else:
        print ('url may be wrong')
        return False





kanunu = 'https://www.kanunu8.com/wuxia/201102/1625.html'
kanunu1 = 'https://www.kanunu8.com/book2/10752/'
tianya = 'http://www.ty2016.net/book/Murakami_13/'
lib99 = 'http://www.99lib.net/book/8007/index.htm'
route(kanunu1)





