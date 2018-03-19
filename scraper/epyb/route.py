import requests
import re
import os
import logging
import string_lib as st
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


# TODO: IMPORTANT:  research how to extract js modified dom
# TODO: IMPORTANT:  把 get title/author/intro 等 function 写成一个
# TODO: IMPORTANT:  之后用OOP的思想重构，每个网站都作为一个class，有各种性质（content/ title/ intro/ author/ etc.）
# TODO: IMPORTANT:  Check compatibility on python 2.7

# TODO：提高目录页的美观程度
# TODO: 进一步探索 epub 的格式规范以创造更符合规矩标准的epub文件
# TODO：思考怎么搞epub的封面图？
# TODO: Think about multi threading
# TODO： Research more on travis CI to manage the program



# Define the relation between index url and each chapter url

def kanunu(all_chapter, href, index, source, url):
    if source == 'kanunu' and href and index in href:
        pos = url.index(index)
        abs_link = url[:pos] + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def kanunu1(all_chapter, href, index, source, url):
    if source == 'kanunu1' and href and '/' not in href:
        if "index.html" in url:
            abs_link = url[:-10]+href
        else:
            abs_link = url + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def ty2016(all_chapter, href, index, source, url):
    if source == 'ty2016' and href and '/' not in href and '.html' in href:
        abs_link = url + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def dushu369(all_chapter, href, index, source, url):
    if source == 'dushu369' and href and index in href and any(char.isdigit() for char in href):
        pos = url.index(index) - 1
        abs_link = url[:pos] + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def txshuku(all_chapter, href, index, source, url):
    if source == 'txshuku' and href and 'chapter' in href:
        abs_link = href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def sfacg(all_chapter, href, index, source, url):
    if source == 'sfacg' and 'Novel' in href and index in href and href.split('/')[-3] != 'Novel':
        url_pos = url.index(index)
        href_pos = href.index(index)
        abs_link = url[:url_pos] + href[href_pos:]
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)

def wenku8()

# Support provides all info about different supported site, the orders are:
# site name (correspond to different method to extract chapter link)/ index/ content/ title/ author/ intro
support = {'kanunu': [kanunu,
                      lambda url : url.split('/')[-1].split('.')[0], # index in url
                      lambda soup: str(soup.find_all('p')[0]), # content
                      lambda soup: soup.find_all('h2')[0].text, # main title
                      lambda soup: soup.find_all('h2')[0].text, # chapter title
                      lambda soup: soup.find_all('td', {'class': 'p10-21'})[0].text, # intro
                      lambda soup: soup.find_all('td')[12].find_all('td')[1].text.split(" ")[1].split("：")[2], # author
                      "努努书坊",
                      "https://www.kanunu8.com/"
                      ],
           'kanunu1':[kanunu1,
                      lambda url : url.split('/')[-2], # index in url
                      lambda soup: str(soup.find_all('p')[0]), # content
                      lambda soup: soup.find_all('h1')[0].text, # main title
                      lambda soup: soup.find_all('font')[0].text, # chapter title
                      lambda soup: soup.find_all('td', {'class': 'p10-24'})[1].text, # intro
                      lambda soup: soup.find_all('td')[12].text.split("：")[1].split(" ")[0],  #author
                      "努努书坊",
                      "https://www.kanunu8.com/"
                      ],
           'ty2016':[ty2016,
                     lambda url : url.split('/')[-2], # index in url
                     lambda soup: str(soup.find_all('p')[1]), # content
                     lambda soup: soup.find_all('h1')[0].text, # main title
                     lambda soup: soup.find_all('h1')[0].text, # chapter title
                     lambda soup: soup.find_all('p')[0].text, # intro
                     lambda soup: soup.find_all('h2')[1].a.text, #author
                     "天涯书库",
                     "http://www.ty2016.net/"
                     ],
           'dushu369':[dushu369,
                       lambda url : url.split('/')[-3], # index in url
                       lambda soup: str(soup.find_all("td", {"class": "content"})[0]), # content
                       lambda soup: soup.find_all('td', {'class':'cntitle'})[0].text.split('《')[1][:-1], # main title
                       lambda soup: soup.find_all('td', {'class':'cntitle'})[0].text, # chapter title
                       lambda soup: soup.find_all('td', {'class':'Readme'})[0].text, # intro
                       lambda soup: soup.find_all('td', {'class':'cntitle'})[0].text.split('《')[0], # author
                       "读书369",
                       "www.dushu369.com"
                       ],
           'txshuku':[txshuku,
                      lambda url : url.split('/')[-1].split('.')[0], # index in url
                      lambda soup: str(soup.find_all('div', {"class":"contentbox"})[0]), # content
                      lambda soup: soup.find_all('h1')[0].text[:-4], # main title
                      lambda soup: soup.find_all('h1')[0].text, # chapter title
                      lambda soup: soup.find_all('p')[1].text, # intro
                      lambda soup: soup.find_all('p')[1].text, # author
                      "天下书库",
                      "http://www.txshuku.net/"
                      ],
           'sfacg':[sfacg,
                    lambda url: url.split('/')[-3], # index in url
                    lambda soup: str(soup.find_all('div', {'id':'ChapterBody'})[0]), # content
                    lambda soup: soup.find_all('h1')[0].text, # main title
                    lambda soup: soup.find_all('h1')[0].text, # chapter title
                    lambda soup: soup.find_all('p', {"class": "summary big-profiles"}),  # TODO: intro <- does not work for now
                    lambda soup: soup.find_all('p', {"class": "summary big-profiles"}), # author
                    "SFACG",
                    "http://www.sfacg.com/"
                    ],
           'wenku8':[], # TODO
           '23qb':[] # TODO
           }

def get_source(url):
    source = ''
    index = ''
    if 'kanunu' in url: # kanunu 1 & 2
        if url.split('/')[-1] and url.split('/')[-1] != "index.html":
            source = 'kanunu'
        else:
            source = 'kanunu1'
    elif 'ty2016' in url:
        source = 'ty2016'
    elif 'dushu369' in url:
        source = 'dushu369'
    elif 'txshuku' in url:
        source = 'txshuku'
    elif 'sfacg' in url:
        source = 'sfacg'
    return source

def parse_index(soup, source, url):
    index = support[source][1](url)
    all_chapter = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if source in support:
            support[source][0](all_chapter, href, index, source, url)
    return all_chapter

# change it the same way as parse index
# /html/body/div[1]/table/tbody/tr/td/table[3]/tbody/tr[3]/td
def get_content(soup, source):

    if source in support:
        return support[source][2](soup)

    # if source == 'dushu369':
    #     #TODO: different way to modify br in dushu 369
    #     content = re.sub('<br/>\n<br/>', '</p>\n<p>', content)
    # else:
    #     content = re.sub('<br/>\n<br/>', '</p>\n<p>', content)
    # return content


def get_title_main(soup, source):
    if source in support:
        return support[source][3](soup)

def get_title_chapter(soup, source):
    if source in support:
        return support[source][4](soup)

def get_intro(soup, source, url):
    if source != 'sfacg' and source in support:
        return support[source][5](soup)
    elif source == 'sfacg':
        # pos = url.index('MainIndex')
        # url = url[:pos]
        # res = requests.get(url)
        # page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        # soup = BeautifulSoup(page, 'html.parser')
        return "SFACG: 尚无法获得作品简介"# support[source][5](soup)

def get_author(soup, source, url):
    if source != 'txshuku' and source != 'sfacg' and source in support:
        return support[source][6](soup)
    elif source == 'txshuku':
        indexurl = url.replace('dir','article')
        res = requests.get(indexurl)
        res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        return support[source][6](soup)
    # TODO
    elif source == 'sfacg':
        return "SFACG: 尚无法获得作者信息"


# loop through all chapter's link, extract the content
def get_epub_content(soup, folder, source, url):

    all_chapters = parse_index(soup, source, url)
    counter = 1
    h0, h1, h20, h21,tail = st.content_header_0, st.content_header_1, st.h20, st.h21, st.tail
    title_dict = {}
    for link in all_chapters:
        res = requests.get(link)
        if source != "sfacg":
            res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        title = (get_title_chapter(soup, get_source(url)))
        title_dict[counter] = title
        content = get_content(soup, get_source(url))
        file_name = 'chapter_' + str(counter) + '.xhtml'
        logging.info("Creating content: %s...", file_name)
        epub_content = h0 + title + h1 + h20 + title + h21 + content + tail
        file = open(folder+'/'+file_name, "wb")
        file.write(epub_content.encode('utf-8'))
        counter += 1
        file.close
    return title_dict

def META_INF(dirname):
    meta_inf_dir = dirname + '/META-INF'
    meta_inf_content = st.meta_inf_content
    os.makedirs(meta_inf_dir, exist_ok=True)
    containxml_path = meta_inf_dir + '/container.xml'
    with open(containxml_path, "w") as f:
        f.write(meta_inf_content)
        f.close()


def catalogxhtml(chapter_dict, title, dirname):
    head1, head2, tail, list1, list2, list3 = st.cat_h1, st.cat_h2, st.cat_tail, st.cat_list1, st.cat_list2, st.cat_list3
    content = head1 + title + head2

    for chapter,title in chapter_dict.items():
        lst = list1 + str(chapter) + list2 + title + list3
        content += lst
    content += tail
    with open(dirname+'/catalog.xhtml', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()


def mimetype(dirname):
    content = 'application/epub+zip'
    with open(dirname + '/mimetype', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()


def contentopf(chapter_dict, title, author, intro, source_site, source_url, dirname):
    head1, head2 = st.opf_h1, st.opf_h2
    dctitle = "<dc:title>"+title+"</dc:title>\n"
    dccreator = "<dc:creator>"+author+"</dc:creator>\n"
    dcintro = "<dc:description>"+intro+"</dc:description>\n"
    dclanguage = "<dc:language>zh-cn</dc:language>\n"
    dccontributor = "<dc:contributor>" + source_site + ' ' + source_url + "</dc:contributor>\n"
    dcpublisher = "<dc:publisher>"+source_url+"</dc:publisher>\n"
    dcsubject = "<dc:subject>"+source_site+"</dc:subject>\n"
    dcidentifier = "<dc:identifier id='bookid'>pymtrdr:000001</dc:identifier>"

    content = head1 + dctitle + dccreator + dcintro + dclanguage + dccontributor + dcpublisher + dcsubject + dcidentifier + head2

    item1, item2, item3 = st.opf_i1, st.opf_i2, st.opf_i3
    idref1, idref2, idref = st.opf_id1, st.opf_id2, st.opf_id

    for chapter, title in chapter_dict.items():
        item = item1 + str(chapter) + item2 + str(chapter) + item3
        content += item
        idref += idref1 + str(chapter) + idref2

    item_other, spine_head, tail = st.opf_io, st.opf_sh, st.opf_tail
    content+= item_other + spine_head + idref + tail

    with open(dirname+'/content.opf', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()


def pagexhtml(title, author, intro, source_site, source_url, dirname):
    head1, head2, head3, head4, head5, head6 = st.px_h1, st.px_h2, st.px_h3, st.px_h4, st.px_h5, st.px_h6
    content = head1 + title + head2 + author + head3 + intro + head4 + source_site + head5 + source_url + head6
    with open(dirname+'/page.xhtml', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()

# TODO: let user modify the format accordingly
def stylesheetcss(dirname):
    content = st.style_c
    with open(dirname+'/stylesheet.css', 'w') as f:
        f.write(content)
        f.close()

def tocncx(chapter_dict, title, author, dirname):
    head1, head2, head3, tail = st.toc_h1, st.toc_h2, st.toc_h3, st.toc_t
    nav1, nav2, nav3, nav4, nav5 = st.toc_n1, st.toc_n2, st.toc_n3, st.toc_n4, st.toc_n5
    content = head1 + title + head2 + author + head3
    for chapter, title in chapter_dict.items():
        content += nav1 +str(chapter)+ nav2 + str(chapter) + nav3 + title + nav4 + str(chapter) + nav5
    content += tail

    with open(dirname+'/toc.ncx', 'wb') as f:
        f.write(content.encode('utf-8'))
        f.close()


def build_epub(url):
    source = get_source(url)
    res = requests.get(url)
    if source != "sfacg":  # corner case, sfacg does not require encoding
        res.encoding = 'gb2312'
    page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
    soup = BeautifulSoup(page, 'html.parser')
    logging.info("Getting title/ author/ intro information...")
    title = get_title_main(soup, source)
    print (title)
    author = get_author(soup, source, url)
    intro = get_intro(soup, get_source(url), url)

    # create directory
    dirname = title
    logging.info("Creating folder...")
    os.makedirs(title, exist_ok= True)

    # write content in the directory
    chapter_dict = get_epub_content(soup, dirname, source, url)  # soup, folder, source, url

    # create meta_inf
    # TODO: a better way might be have a META-INF folder ready and copy it to other epub folders since META-INF never changes
    logging.info("Creating META_INF file...")
    META_INF(dirname)

    # create catelog.xhtml
    logging.info("Creating catelog.xhtml...")
    catalogxhtml(chapter_dict, title, dirname)

    # create mimetype
    # TODO: a better way might be have a mimetype folder ready and copy it to other epub folders since mimetype never changes
    logging.info("Creating MIMETYPE")
    mimetype(dirname)

    # create content.opf
    logging.info("Creating content.opf...")
    source = get_source(url)
    source_site = support[source][7]
    source_url = support[source][8]
    contentopf(chapter_dict, title, author, intro, source_site, source_url, dirname)

    # create page.xhtml
    logging.info("Creating page.xthml...")
    pagexhtml(title, author, intro, source_site, source_url, dirname)

    # create stylesheet.css
    logging.info("Creating stylesheet.css...")
    stylesheetcss(dirname)

    # create tocncx
    logging.info("Creating toc.ncx...")
    tocncx(chapter_dict, title, author, dirname)

    return title

if __name__ == "__main__":


    kanunu_index = 'https://www.kanunu8.com/files/yqxs/201103/1863.html'
    kanunu1_index = 'https://www.kanunu8.com/book/4333/'
    kc = 'https://www.kanunu8.com/files/yqxs/201103/1863/43617.html'
    kc1 = 'https://www.kanunu8.com/book/4333/51335.html'

    shaqiu_index = "https://www.kanunu8.com/book3/6425/index.html"

    ty2016_index = 'http://www.ty2016.net/book/Murakami_13/'
    tc = 'http://www.ty2016.net/book/Murakami_13/67710.html'

    dushu369_index = 'http://www.dushu369.com/waiguomingzhu/bngd/'
    dc = 'http://www.dushu369.com/waiguomingzhu/HTML/63294.html'

    txshuku_index = 'http://book.txshuku.net/dir/352.html'
    txc = 'http://book.txshuku.net/chapter/352/29636.html'

    sfacg_index = 'http://book.sfacg.com/Novel/108421/MainIndex/'
    sc = 'http://book.sfacg.com/Novel/108421/183067/1512447/'

    # Test build epub

    build_epub(kanunu_index)

    # Test each function

    # url = sc
    # source = get_source(url)
    # res = requests.get(url)
    # # res.encoding = 'gb2312'
    # page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
    # soup = BeautifulSoup(page, 'html.parser')
    #
    # content = get_content(soup, source)
    # print (content)
    # title = get_title_main(soup, source)
    # print (title)
    # title = get_title_chapter(soup, source)
    # print(title)
    # print(get_intro(soup, source, url))
    # print (get_author(soup, source, url))







