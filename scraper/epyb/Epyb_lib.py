# Put all files in one

# Step 1:  Search the book name on google

from googleapiclient.discovery import build

# google api: AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4
# cse id: 006143628057480232827:4svfte2xdd4

# return the first url from google search
def search_ask(name):
    # build a service object for interacting with api.
    service = build("customsearch", "v1", developerKey="AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4")
    res = service.cse().list(
        q=name,
        cx='006143628057480232827:4svfte2xdd4',
    ).execute()

    # If no results found
    if int(res['queries']['request'][0]['totalResults']) == 0:
        print ('No result found')
        return False

    return res['items'][0]['link']


# Step 2: scrape the site and fetch the contents

import requests
import re
import os
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


####################################################
# Helper functions
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
        abs_link = url[:url.index(index)-1] + href
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


def wenku8(all_chapter, href, index, source, url):
    if source == 'wenku8' and href and href.split(".")[0].isdigit() and href.split(".")[1] == "htm": # better with regex
        url_pos = url.index(index)
        abs_link = url[:url_pos]+index+'/'+href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


# TODO
def qb23():
    pass

# Support uses a dict to contain all info about different sites, the orders are:
support = {'kanunu': [kanunu,
                      lambda url : url.split('/')[-1].split('.')[0], # index in url
                      lambda soup: str(soup.find_all('p')[0]), # content
                      lambda soup: soup.find_all('h2')[0].text, # book title
                      lambda soup: soup.find_all('h2')[0].text, # chapter title
                      lambda soup: soup.find_all('td', {'class': 'p10-21'})[0].text, # intro
                      lambda soup: soup.find_all('td')[12].find_all('td')[1].text.split(" ")[1].split("：")[2], # author
                      "努努书坊",
                      "https://www.kanunu8.com/"
                      ],
           'kanunu1':[kanunu1,
                      lambda url : url.split('/')[-2], # index in url
                      lambda soup: str(soup.find_all('p')[0]), # content
                      lambda soup: soup.find_all('h1')[0].text, # book title
                      lambda soup: soup.find_all('font')[0].text, # chapter title
                      lambda soup: soup.find_all('td', {'class': 'p10-24'})[1].text, # intro
                      lambda soup: soup.find_all('td')[12].text.split("：")[1].split(" ")[0],  #author
                      "努努书坊",
                      "https://www.kanunu8.com/"
                      ],
           'ty2016':[ty2016,
                     lambda url : url.split('/')[-2], # index in url
                     lambda soup: str(soup.find_all('p')[1]), # content
                     lambda soup: soup.find_all('h1')[0].text, # book title
                     lambda soup: soup.find_all('h1')[0].text, # chapter title
                     lambda soup: soup.find_all('p')[0].text, # intro
                     lambda soup: soup.find_all('h2')[1].a.text, #author
                     "天涯书库",
                     "http://www.ty2016.net/"
                     ],
           'dushu369':[dushu369,
                       lambda url : url.split('/')[-3], # index in url
                       lambda soup: str(soup.find_all("td", {"class": "content"})[0]), # content
                       lambda soup: soup.find_all('td', {'class':'cntitle'})[0].text.split('《')[1][:-1], # book title
                       lambda soup: soup.find_all('td', {'class':'cntitle'})[0].text, # chapter title
                       lambda soup: soup.find_all('td', {'class':'Readme'})[0].text, # intro
                       lambda soup: soup.find_all('td', {'class':'cntitle'})[0].text.split('《')[0], # author
                       "读书369",
                       "www.dushu369.com"
                       ],
           'txshuku':[txshuku,
                      lambda url : url.split('/')[-1].split('.')[0], # index in url
                      lambda soup: str(soup.find_all('div', {"class":"contentbox"})[0]), # content
                      lambda soup: soup.find_all('h1')[0].text[:-4], # book title
                      lambda soup: soup.find_all('h1')[0].text, # chapter title
                      lambda soup: soup.find_all('p')[1].text, # intro
                      lambda soup: soup.find_all('p')[1].text, # author
                      "天下书库",
                      "http://www.txshuku.net/"
                      ],
           'sfacg':[sfacg,
                    lambda url: url.split('/')[-3], # index in url
                    lambda soup: str(soup.find_all('div', {'id':'ChapterBody'})[0]), # content
                    lambda soup: soup.find_all('h1')[0].text, # book title
                    lambda soup: soup.find_all('h1')[0].text, # chapter title
                    lambda soup: soup.find_all('p', {"class": "summary big-profiles"}).text,  # TODO: intro <- does not work for now
                    lambda soup: soup.find_all('p', {"class": "summary big-profiles"}).text, # author
                    "SFACG",
                    "http://www.sfacg.com/"
                    ],
           'wenku8':[wenku8,
                     lambda url: url.split('/')[-2],  # index in url
                     lambda soup: str(soup.find_all('div', {'id': 'content'})[0]),  # content #TODO: unneeded ul included
                     lambda soup: soup.find_all('div', {'id': 'title'})[0].text,  # book title
                     lambda soup: soup.find_all('div', {'id': 'title'})[0].text,  # chapter title
                     lambda soup: soup.find_all('span', {"style": "font-size:14px;"})[1].text,  # Intro # Important: url changed
                     lambda soup: soup.find_all('div', {'id': 'info'})[0].text.split("：")[1],  # author
                     "轻小说文库",
                     "http://www.wenku8.com/"
                     ],
           '23qb':[qb23,
                   lambda url: url.split('/')[-3],  # index in url
                   lambda soup: str(soup.find_all('div', {'id': 'ChapterBody'})[0]),  # content
                   lambda soup: soup.find_all('h1')[0].text,  # book title
                   lambda soup: soup.find_all('h1')[0].text,  # chapter title
                   lambda soup: soup.find_all('p', {"class": "summary big-profiles"}),
                   lambda soup: soup.find_all('p', {"class": "summary big-profiles"}),  # author
                   "SFACG",
                   "http://www.sfacg.com/"
                   ], # TODO
           }
####################################################


# Check the url and analyze which site it comes from
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
    elif 'wenku8' in url:
        source = 'wenku8'
    elif '23qb' in url:
        source = 'qb23'
    else:
        return False
    return source


def site_parse(source, url):
    res = requests.get(url)
    if source == "wenku8":
        res.encoding = 'gbk'
    elif source == "sfacg":
        pass
    else:
        res.encoding = 'gb2312'
    page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def parse_index(soup, source, url):
    index = support[source][1](url)
    all_chapter = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if source in support:
            support[source][0](all_chapter, href, index, source, url)
    return all_chapter


def get_content(soup, source):

    if source in support:
        return support[source][2](soup)


def get_title_main(soup, source):
    if source in support:
        return support[source][3](soup)


def get_title_chapter(soup, source):
    if source in support:
        return support[source][4](soup)


def get_author(soup, source, url):
    if source != 'txshuku' and source != 'sfacg' and source in support:
        return support[source][6](soup)
    elif source == 'txshuku':
        indexurl = url.replace('dir','article')

        soup = site_parse(source, indexurl)
        return support[source][6](soup)
    # TODO
    elif source == 'sfacg':
        return "SFACG: 尚无法获得作者信息"


def get_intro(soup, source, url):
    if source in support:
        if source == 'sfacg':
            return "SFACG: 尚无法获得作品简介"  # support[source][5](soup)
        elif source == 'wenku8':
            return wenku8_intro(url)
        else:
            return support[source][5](soup)


# helper function for wenku8's intro since its in a different webpage
def wenku8_intro(url):
    source = 'wenku8'
    new_url = "/".join(url.split('/')[:-3]).replace("novel", "book") + '/' + url.split('/')[-2] + '.htm'

    soup = site_parse(source, new_url)
    return soup.find_all('span', {"style": "font-size:14px;"})[1].text


# loop through all chapter's link, extract the content
def get_epub_content(soup, folder, source, url):

    all_chapters = parse_index(soup, source, url)
    counter = 1
    h0, h1, h20, h21,tail = _content_header_0, _content_header_1, _h20, _h21, _tail
    title_dict = {}
    for link in all_chapters:

        soup = site_parse(source, link)
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
    meta_inf_content = _meta_inf_content
    os.makedirs(meta_inf_dir, exist_ok=True)
    containxml_path = meta_inf_dir + '/container.xml'
    with open(containxml_path, "w") as f:
        f.write(meta_inf_content)
        f.close()


def catalogxhtml(chapter_dict, title, dirname):
    head1, head2, tail, list1, list2, list3 = _cat_h1, _cat_h2, _cat_tail, _cat_list1, _cat_list2, _cat_list3
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


# TODO: need a rewrite?
def contentopf(chapter_dict, title, author, intro, source_site, source_url, dirname):
    head1, head2 = _opf_h1, _opf_h2
    dctitle = "<dc:title>"+title+"</dc:title>\n"
    dccreator = "<dc:creator>"+author+"</dc:creator>\n"
    dcintro = "<dc:description>"+intro+"</dc:description>\n"
    dclanguage = "<dc:language>zh-cn</dc:language>\n"
    dccontributor = "<dc:contributor>" + source_site + ' ' + source_url + "</dc:contributor>\n"
    dcpublisher = "<dc:publisher>"+source_url+"</dc:publisher>\n"
    dcsubject = "<dc:subject>"+source_site+"</dc:subject>\n"
    dcidentifier = "<dc:identifier id='bookid'>pymtrdr:000001</dc:identifier>"

    content = head1 + dctitle + dccreator + dcintro + dclanguage + dccontributor + dcpublisher + dcsubject + dcidentifier + head2

    item1, item2, item3 = _opf_i1, _opf_i2, _opf_i3
    idref1, idref2, idref = _opf_id1, _opf_id2, _opf_id

    for chapter, title in chapter_dict.items():
        item = item1 + str(chapter) + item2 + str(chapter) + item3
        content += item
        idref += idref1 + str(chapter) + idref2

    item_other, spine_head, tail = _opf_io, _opf_sh, _opf_tail
    content+= item_other + spine_head + idref + tail

    with open(dirname+'/content.opf', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()


def Images(dirname):
    images_dir = dirname + '/Images'
    os.makedirs(images_dir, exist_ok=True)


def pagexhtml(title, author, intro, source_site, source_url, dirname):
    head1, head2, head3, head4, head5, head6 = _px_h1, _px_h2, _px_h3, _px_h4, _px_h5, _px_h6
    content = head1 + title + head2 + author + head3 + intro + head4 + source_site + head5 + source_url + head6
    with open(dirname+'/page.xhtml', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()

# TODO: let user modify the format
def stylesheetcss(dirname):
    content = _style_c
    with open(dirname+'/stylesheet.css', 'w') as f:
        f.write(content)
        f.close()

def tocncx(chapter_dict, title, author, dirname):
    head1, head2, head3, tail = _toc_h1, _toc_h2, _toc_h3, _toc_t
    nav1, nav2, nav3, nav4, nav5 = _toc_n1, _toc_n2, _toc_n3, _toc_n4, _toc_n5
    content = head1 + title + head2 + author + head3
    for chapter, title in chapter_dict.items():
        content += nav1 +str(chapter)+ nav2 + str(chapter) + nav3 + title + nav4 + str(chapter) + nav5
    content += tail

    with open(dirname+'/toc.ncx', 'wb') as f:
        f.write(content.encode('utf-8'))
        f.close()


def build_epub(url):
    source = get_source(url)
    soup= site_parse(source, url)
    logging.info("Getting title/ author/ intro information...")
    title = get_title_main(soup, source)
    print(title)
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

    # create folder for images
    logging.info("Creating images folder")
    Images(dirname)

    # create content.opf
    logging.info("Creating content.opf...")
    # source = get_source(url)
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


# Step 3: Compress the folder of book just being created.
import zipfile
import shutil

def zipdir(path, ziph, name):
    # ziph is zipfile handle

    # This method only copy all *files*
    for root, dirs, files in os.walk(path):
        os.chdir(name)
        # TODO: More folders to be compressed
        ziph.write('META-INF/container.xml')
        for file in files:
            ziph.write(file)

def compress(name):
    epub_name = name + '.epub'
    logging.info("Compressing all files and convert to epub...")
    zipf = zipfile.ZipFile(epub_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(name, zipf, name)
    zipf.close()
    logging.info("Delete the unneeded folder...")
    os.chdir("..")
    shutil.rmtree(name)
    logging.info("Done")
    # The idea is to move the file is certain folder after checking that folder does not contain the file
    # cwd = os.getcwd()
    #
    # if not file_in_dir(os.path.join(cwd, "\\book")):
    #     shutil.move(epub_name, os.path.join(cwd, "\\book"))
    return epub_name


# Step 4: Integration

def create(book_name):
    if book_name == '':
        book_name = input("Please enter a book's name: ")
    link = search_ask(book_name)
    folder = build_epub(link)
    real_name = compress(folder)
    return real_name

#### Original string library #####

_content_header_0 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n" \
                   "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'"" 'http:" \
                   "//www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns=" \
                   "'http://www.w3.org/1999/xhtml'" \
                   " xml:lang='zh-CN'>\n<head>\n<title>"
_content_header_1 = "</title>\n<link href='stylesheet.css' type='text/css' rel='stylesheet'/>\n" \
                   "<style type='text/css'>@page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style>\n" \
                   "</head>\n" \
                   "<body>\n"
_h20 = "<h2>\n<span style='border-bottom:1px solid'>"
_h21 = "</span>\n</h2>\n<p>"
_tail = "</p>\n<div class='mbppagebreak'></div></body></html>"
_meta_inf_content = "<?xml version='1.0'?>\n<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:" \
                       "container'>\n<rootfiles>\n<rootfile full-path='content.opf' media-type='application/oe" \
                       "bps-package+xml'/>\n</rootfiles>\n</container>"
_cat_h1 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN" \
            "' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='" \
            "zh-CN'>\n<head>\n<title>"
_cat_h2 = "</title>\n<link href='stylesheet.css' type='text/css' rel='stylesheet'/><style type='text/css'>\n@page " \
            "{ margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style>\n</head>\n<body>\n<h1>目录<br/>Content</h1>\n<ul>"
_cat_tail = "</ul>\n<div class='mbppagebreak'></div>\n</body>\n</html>"
_cat_list1 = "<li class='catalog'><a href='chapter_"
_cat_list2 = ".xhtml'>"
_cat_list3 = "</a></li>\n"
_opf_h1 = "<?xml version='1.0' encoding='utf-8'?>\n\n<package xmlns='http://www.idpf.org/2007/opf' " \
            "xmlns:dc='http://purl.org/dc/elements/1.1/' unique-identifier='bookid' version='2.0'>\n\n " \
            " <metadata xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:opf='http://www.idpf.org/2007/opf'>\n"
_opf_h2 = "</metadata>\n\n<manifest>"
_opf_i1 = "<item href='chapter_"
_opf_i2 = ".xhtml' id='id"
_opf_i3 = "' media-type='application/xhtml+xml'/>\n"
_opf_id1 = "<itemref idref='id"
_opf_id2 = "'/>\n"
_opf_id = ""
_opf_io = "<item href='catalog.xhtml' id='catalog' media-type='application/xhtml+xml'/>\n<item href='stylesheet." \
                 "css' id='css' media-type='text/css'/>\n<item href='page.xhtml' id='page' media-type='application/xhtm" \
                 "l+xml'/>\n<item href='toc.ncx' media-type='application/x-dtbncx+xml' id='ncx'/>\n</manifest>"

_opf_sh = "<spine toc='ncx'>\n<itemref idref='page'/>\n<itemref idref='catalog'/>\n"
_opf_tail = "<itemref idref='page'/>\n</spine>\n\n<guide>\n<reference href='catalog.xhtml' type='toc' title='目录'/>" \
           "\n</guide>\n</package>"

_px_h1 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'" \
            " 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='" \
            "zh-CN'>\n<head>\n<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>\n<title>书籍信息</title>\n" \
            "<style type='text/css' title='override_css'>\n@page {padding: 0pt; margin:0pt}\nbody { text-align: left;" \
            " padding:0pt; margin: 0pt;font-size: 1.0em}\nul,li{list-style-type:none;margin:0;padding:0;line-height:" \
            " 2.5em;font-size: 0.8em}\ndiv,h1,h2 { margin: 0pt; padding: 0pt}\nh1{font-size:1.2em}\nh2 {font-size: 1.1em}" \
            "\n.copyright{color:#ff4500}\n</style>\n</head>\n<body>\n<div>\n<h1>"
_px_h2 = "</h1>\n<h2>作者："
_px_h3 = "</h2>\n<ul>\n<li>内容简介："
_px_h4 ="</li>\n<li class='copyright'>由 epyb 开源项目提供 epub 下载，现支持将部分中文在线阅读网站的书库直接转成 epub 格式。\
    \n可访问 https://github.com/RioAraki/multi_reader 查看详情。\n欢迎 fork, star, 提 issue 等。</li>\n<li class='copyright'>书籍内容由"
_px_h5 = "提供，请访问："
_px_h6 = "</li>\n</ul>\n</div>\n</body>\n</html>"
_style_c = "body{margin:10px;font-size:1em}ul,li{list-style-type:none;margin:0;padding:0}p{text-indent:2em;line-" \
              "height:1.5em;margin-top:0;margin-bottom:1.5em}.catalog{line-height:2.5em;font-size:.8em}li{border-bot" \
              "tom:1px solid #D5D5D5}h1{font-size:1.6em;font-weight:700}h2{display:block;font-size:1.2em;font-weight" \
              ":700;margin-bottom:.83em;margin-left:0;margin-right:0;margin-top:1em}.mbppagebreak{display:block;marg" \
              "in-bottom:0;margin-left:0;margin-right:0;margin-top:0}a{color:inherit;text-decoration:none;cursor:def" \
              "ault}a[href]{color:blue;text-decoration:none;cursor:pointer}.italic{font-style:italic}"
_toc_h1 = "<?xml version='1.0' encoding='utf-8'?>\n<ncx xmlns='http://www.daisy.org/z3986/2005/ncx/' version='2005-1'>\n" \
            "<head>\n<meta content='pymtrdr:000001' name='dtb:uid'/>\n<meta content='2' name='dtb:depth'/>\n<meta content='0' name='dtb:totalPageCount'/>\n" \
            "<meta content='0' name='dtb:maxPageNumber'/>\n</head>\n<docTitle>\n<text>"
_toc_h2 = "</text>\n</docTitle>\n\n<docAuthor>\n<text>"
_toc_h3 = "</text>\n</docAuthor>\n\n<navMap>"
_toc_t = "</navMap>\n\n</ncx>"
_toc_n1 = "<navPoint id='chapter_"
_toc_n2 = "' playOrder='"
_toc_n3 = "'><navLabel><text>"
_toc_n4 = "</text></navLabel><content src='chapter_"
_toc_n5 = ".xhtml'/></navPoint>\n"

##################################

if __name__ == '__main__':

    create(input('please type in the book name you wabt to download:'))

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

    wenku8_index = 'http://www.wenku8.com/novel/2/2353/index.htm'
    wenku8 = 'http://www.wenku8.com/novel/2/2353/86813.htm'

    qb23_index = 'https://www.23qb.com/book/3404/'
    qb23 = 'https://www.23qb.com/book/3404/969333.html'

    build_epub(wenku8_index)

    # Test each function

    # url = wenku8
    # source = get_source(url)
    # res = requests.get(url)
    # res.encoding = 'gb2312'
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