import requests
import re
import os
from bs4 import BeautifulSoup

# TODO: 添加对duhsu369的支持

def get_source(url):
    if 'kanunu' in url:
        if url.split('/')[-1] and 'index' not in url.split('/')[-1]:
            return 'kanunu'
        else:
            return 'kanunu1'
    elif 'ty2016' in url:
        return 'ty2016'
    elif '99lib' in url:
        return '99lib'
    return False

# 有一个 parse link 的潜在问题，https://www.kanunu8.com/book2/10741/可以正确 parse，但https://www.kanunu8.com/book2/10741/index.html无法正确parse
def parse_index(soup, book_idx, url):
    all_chapter = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if url.split('/')[-1]: # format like 'https://www.kanunu8.com/wuxia/201102/1625.html'
            if href and book_idx in href:
                if book_idx in url:
                    if 'kanunu' in url:
                        pos = url.index(book_idx)
                        abs_link = url[:pos] + href
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

# TODO: 回头可以思考怎么重构一下，改成input 为 soup rather than url，以及这个function可能没必要
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
        content = str(soup.body.div.find_all('table')[4].find_all('td')[1].p)
    elif source == 'kanunu1':
        content = str(soup.find_all('p')[0])
    elif source == 'ty2016':
        content = str(soup.find_all('p')[1])
    elif source == '99lib':
        content = soup.find_all('p') # TODO: see how to extract lib99's content
    content = re.sub('<br/>\n<br/>', '</p>\n<p>', content)
    return content


def get_title(soup, source):
    if source == 'kanunu' or source == 'kanunu1' or source == '99lib':
        title = soup.find_all('h2')[0].text
    elif source == 'ty2016':
        title = soup.find_all('h1')[0].text
    return title


def get_intro(soup, source):
    if source == 'kanunu':
        #/html/body/div[1]/table[9]/tbody/tr/td[2]/table[4]/tbody/tr/td/table[1]/tbody/tr/td[2]/text()
        intro = soup.find_all('td')[16].find_all('td')[1].text
    elif source == 'ty2016':
        # //*[@id="main"]/div[2]/div[2]/p/text()
        intro = soup.find('div', {'id': 'main'}).find_all('p')[0].text
    elif source == 'kanunu1':
        # /html/body/div[1]/table[9]/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/text()
        intro = soup.find_all('td')[16].text
    elif source == 'dushu369':
        pass
    if intro:
        return intro
    return False


def get_author(soup, source):
    if source == 'kanunu':
        author = soup.find_all('td')[12].find_all('td')[1].text.split(" ")[1].split("：")[2] # Note to use chinese "："
    elif source == 'kanunu1':
        author = soup.find_all('td')[12].text.split("：")[1].split(" ")[0]
    elif source == 'ty2016':
        author =soup.find_all('h2')[1].a.text
    elif source == 'dushu369':
        pass
    if author:
        return author
    return False


def write_in_md(url):
    all_chapters = route(url)
    file = open("test.md","wb")  # The wb indicates that the file is opened for writing in binary mode.
    for link in all_chapters:
        res = requests.get(link)
        res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        title = ('<br/>##' + get_title(soup, get_source(url))).encode('utf-8')
        content = get_content(soup, get_source(url)).encode('utf-8')
        file.write(title)
        file.write(content)
    file.close()


def get_epub_content(url, folder):
    all_chapters = route(url)
    counter = 1
    header0 = "<?xml version='1.0' encoding='utf-8' standalone='no'?><!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'" \
             " 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'><html xmlns='http://www.w3.org/1999/xhtml'" \
             " xml:lang='zh-CN'><head><title>"
    header1 = "</title><link href='stylesheet.css' type='text/css' rel='stylesheet'/><style type='text/css'>@page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style></head><body>"
    h20 = "<h2><span style='border-bottom:1px solid'>"
    h21 = "</span></h2><p>"
    tail = "</p><div class='mbppagebreak'></div></body></html>"
    title_dict = {}
    for link in all_chapters:
        res = requests.get(link)
        res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        title = (get_title(soup, get_source(url)))
        title_dict[counter] = title
        content = get_content(soup, get_source(url))
        file_name = 'chapter_' + str(counter) + '.xhtml'
        epub_content = header0 + title + header1 + h20 + title + h21 + content + tail
        file = open(folder+'/'+file_name, "wb")
        file.write(epub_content.encode('utf-8'))
        counter += 1
        file.close
    return title_dict

def META_INF(dirname):
    meta_inf_dir = dirname + '/META-INF'
    meta_inf_content = "<?xml version='1.0'?><container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:" \
                       "container'><rootfiles><rootfile full-path='content.opf' media-type='application/oe" \
                       "bps-package+xml'/></rootfiles></container>"
    os.makedirs(meta_inf_dir, exist_ok=True)
    containxml_path = meta_inf_dir + '/container.xml'
    with open(containxml_path, "w") as f:
        f.write(meta_inf_content)


def catalogxhtml(chapters, title):
    head1 = "<?xml version='1.0' encoding='utf-8' standalone='no'?><!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN" \
            "' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='" \
            "zh-CN'><head><title>"
    head2 = "</title><link href='stylesheet.css' type='text/css' rel='stylesheet'/><style type='text/css'>@page " \
            "{ margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style></head><body><h1>目录<br/>Content</h1><ul>"

def build_epub(url):
    res = requests.get(url)
    res.encoding = 'gb2312'
    page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
    soup = BeautifulSoup(page, 'html.parser')
    title = get_title(soup, get_source(url))
    author = get_author(soup, get_source(url))
    intro = get_intro(soup, get_source(url))

    # create directory
    dirname = title
    os.makedirs(title, exist_ok= True)

    # write content in the directory
    chapter_dict = get_epub_content(url, dirname)

    # create meta_inf
    # TODO: a better way might be have a META-INF folder ready and copy it to other epub folders since META-INF neever changes
    META_INF(dirname)

    # create catelog.xhtml





if __name__ == "__main__":

    kanunu = 'https://www.kanunu8.com/wuxia/201102/1625.html'
    kanunu1 = 'https://www.kanunu8.com/book2/10752/'
    kanunu1_1 = 'https://www.kanunu8.com/book2/10741/'
    ty2016 = 'http://www.ty2016.net/book/Murakami_13/'
    lib99 = 'http://www.99lib.net/book/8007/index.htm'

    # Test build epub
    build_epub(kanunu)




    # # TEST EPUB
    # # get_epub_content(ty2016)
    #
    # # TEST get_intro/ get_author
    # url = ty2016
    # res = requests.get(url)
    # res.encoding = 'gb2312'
    # page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
    # soup = BeautifulSoup(page, 'html.parser')
    # get_author(soup, get_source(url))
    # # get_intro(soup, get_source(url))











