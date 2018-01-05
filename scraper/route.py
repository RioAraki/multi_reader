import requests
import re
from bs4 import BeautifulSoup


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
            if href and '/' not in href:
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

def write_in(url):
    all_chapters = route(url)
    file = open("test.txt","wb")  # The wb indicates that the file is opened for writing in binary mode.
    for link in all_chapters:
        print (link)
        res = requests.get(link)
        res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        if source(url) == 'kanunu':
            title = soup.body.find_all('h2')[0].text#.encode('utf-8')
            content = soup.body.div.find_all('table')[4].find_all('td')[1].p.text#.encode('utf-8')
        elif source(url) == 'kanunu1':
            # /html/body/div[1]/table[8]/tbody/tr[1]/td/h2/font
            title = soup.body.find_all('h2')[0].text#.encode('utf-8')
            content = soup.find_all('p')[0].text#.encode('utf-8')
        elif source(url) == 'ty2016':
            title = soup.body.find_all('h1')[0].text#.encode('utf-8')
            content = soup.find_all('p')[1].text.encode('utf-8')
        elif source(url) == '99lib':
            content = soup.find_all('p')
        print (title)
        print (content)
        #file.write(content)

    file.close()



if __name__ == "__main__":

    kanunu = 'https://www.kanunu8.com/wuxia/201102/1625.html'
    kanunu1 = 'https://www.kanunu8.com/book2/10752/'
    ty2016 = 'http://www.ty2016.net/book/Murakami_13/'
    lib99 = 'http://www.99lib.net/book/8007/index.htm'
    # kanunu path: /html/body/div/table[5]/tbody/tr/td[2]/p
    write_in(ty2016)









