import requests
import re
from bs4 import BeautifulSoup

# TODO: 添加对duhsu369的支持

def source(url):

    if 'kanunu' in url:
        if url.split('/')[-1]:
            return 'kanunu'
        else:
            return 'kanunu1'
    elif 'ty2016' in url:
        return 'ty2016'
    elif '99lib' in url:
        return '99lib'
    return False


def parse_index(soup, book_idx, url):
    all_chapter = []

    for link in soup.find_all('a'):
        href = link.get('href')
        print (href)
        if url.split('/')[-1]: # format like 'https://www.kanunu8.com/wuxia/201102/1625.html'
            if href and book_idx in href:
                if book_idx in url:
                    if 'kanunu' in url:
                        pos = url.index(book_idx)
                        abs_link = url[:pos] + href
                    elif '99lib' in url and 'm.99lib.net' not in href:
                        abs_link = 'http://www.99lib.net' + href
                    if abs_link not in all_chapter:
                        all_chapter.append(abs_link)
        else: # format like 'https://www.kanunu8.com/book2/10752/'
            if href and '/' not in href and '.html' in href:
                abs_link = url + href
                all_chapter.append(abs_link)
    return all_chapter


def find_index(url):
    if '99lib' in url:
        return url.split('/')[-2]
    elif 'kanunu' or 'ty2016' in url:
        if url.split('/')[-1]: # 'https://www.kanunu8.com/wuxia/201102/1625.html'
            return url.split('/')[-1].split('.')[0]
        else:
            return url.split('/')[-2]
    else:
        print ('unable to find index from the url given')
        return False


def route(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    book_idx = find_index(url)
    if 'kanunu' in url or 'ty2016' in url or '99lib' in url:
        return parse_index(soup, book_idx, url)
    print ('only accept url from kanunu/ tianya/ 99lib')
    return False


def get_content(soup, source):
    if source == 'kanunu':
        content = soup.body.div.find_all('table')[4].find_all('td')[1].p.text.encode('utf-8')
    elif source == 'kanunu1':
        content = soup.find_all('p')[0].text
    elif source == 'ty2016':
        content = soup.find_all('p')[1].text
    elif source == '99lib':
        content = soup.find_all('p') # TODO: see how to extract lib99's content
    return content


def get_title(soup, source):
    if source == 'kanunu' or source == 'kanunu1' or source == '99lib':
        title = soup.find_all('h2')[0].text
    elif source == 'ty2016':
        title = soup.find_all('h1')[0].text
    return title


def write_in_md(url):
    all_chapters = route(url)
    file = open("test.md","wb")  # The wb indicates that the file is opened for writing in binary mode.
    for link in all_chapters:
        res = requests.get(link)
        res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        title = ('<br/>##' + get_title(soup, source(url))).encode('utf-8')
        content = get_content(soup, source(url)).encode('utf-8')
        file.write(title)
        file.write(content)
    file.close()

def get_epub(url):
    all_chapters = route(url)
    counter = 1
    header0 = "<?xml version='1.0' encoding='utf-8' standalone='no'?><!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'" \
             " 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'><html xmlns='http://www.w3.org/1999/xhtml'" \
             " xml:lang='zh-CN'><head><title>"
    header1 = "</title><link href='stylesheet.css' type='text/css' rel='stylesheet'/><style type='text/css'>@page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style></head><body>"
    h20 = "<h2><span style='border-bottom:1px solid'>"
    h21 = "</span></h2><p>"
    tail = "</p><div class='mbppagebreak'></div></body></html>"


    for link in all_chapters:

        res = requests.get(link)
        res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        title = (get_title(soup, source(url)))
        content = get_content(soup, source(url))
        file_name = 'chapter_' + str(counter) + '.xhtml'
        epub_content = header0 + title + header1 + h20 + title + h21 + content + tail

        file = open(file_name, "wb")
        file.write(epub_content.encode('utf-8'))
        counter += 1
        file.close





if __name__ == "__main__":

    kanunu = 'https://www.kanunu8.com/wuxia/201102/1625.html'
    kanunu1 = 'https://www.kanunu8.com/book2/10752/'
    ty2016 = 'http://www.ty2016.net/book/Murakami_13/'
    lib99 = 'http://www.99lib.net/book/8007/index.htm'

    get_epub(ty2016)









