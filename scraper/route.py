import requests
import re
import os
from bs4 import BeautifulSoup

# TODO: 由于之后可能会支持的小说网站众多，所以需要重构源头选择部分，以有更好的可拓展性
# TODO：最好全程只需要输入url一次，之后尽量用soup

# TODO: [重要]  之后用OOP的思想重构，每个网站都作为一个class，有各种性质（content/ title/ intro/ author/ etc.）




# Current supported list:

# kanunu8: 1. https://www.kanunu8.com/files/yqxs/201103/1863.html  2. https://www.kanunu8.com/book/4333/
# content: 1. https://www.kanunu8.com/files/yqxs/201103/1863/43617.html 2. https://www.kanunu8.com/book/4333/51335.html

# ty2016: 1. http://www.ty2016.net/book/Murakami_13/
# content: 1.http://www.ty2016.net/book/Murakami_13/67710.html

# dushu369: 1. http://www.dushu369.com/waiguomingzhu/bngd/
# content: 1. http://www.dushu369.com/waiguomingzhu/HTML/63294.html

# txshuku: 1. http://book.txshuku.net/dir/352.html
# content: 1. http://book.txshuku.net/chapter/352/29636.html

# sfacg: 1. http://book.sfacg.com/Novel/108421/MainIndex/
# content: 1. http://book.sfacg.com/Novel/108421/183067/1512447/
# TODO: [重要]  research how to extract js modified dom
# TODO: [重要]  把get title/author/intro等function写成一个


def kanunu(all_chapter, href, index):
    if source == 'kanunu' and href and index in href:
        pos = url.index(index)
        abs_link = url[:pos] + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def kanunu1(all_chapter, href, index):
    if source == 'kanunu1' and href and '/' not in href:
        abs_link = url + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)



def ty2016(all_chapter, href, index):
    if source == 'ty2016' and href and '/' not in href and '.html' in href:
        abs_link = url + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def dushu369(all_chapter, href, index):
    if source == 'dushu369' and href and index in href and any(char.isdigit() for char in href):
        pos = url.index(index) - 1
        abs_link = url[:pos] + href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def txshuku(all_chapter, href, index):
    if source == 'txshuku' and href and 'chapter' in href:
        abs_link = href
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)


def sfacg(all_chapter, href, index):
    if source == 'sfacg' and 'Novel' in href and index in href and href.split('/')[-3] != 'Novel':
        url_pos = url.index(index)
        href_pos = href.index(index)
        abs_link = url[:url_pos] + href[href_pos:]
        if abs_link not in all_chapter:
            all_chapter.append(abs_link)

# Support provides all info about different supported site, the orders are:
# site name (correspond to different method to extract chapter link)/ index/ content/ title/ author/ intro
support = {'kanunu': [kanunu,
                      lambda: url.split('/')[-1].split('.')[0], # index in url
                      lambda: str(soup.find_all('p')[0]), # content
                      lambda: soup.find_all('h2')[0].text, # main title
                      lambda: soup.find_all('h2')[0].text, # chapter title
                      lambda: soup.find_all('td', {'class': 'p10-21'})[0].text, # intro
                      lambda: soup.find_all('td')[12].find_all('td')[1].text.split(" ")[1].split("：")[2] # author
                      ],
           'kanunu1':[kanunu1,
                      lambda: url.split('/')[-2], # index in url
                      lambda: str(soup.find_all('p')[0]), # content
                      lambda: soup.find_all('h1')[0].text, # main title
                      lambda: soup.find_all('font')[0].text, # chapter title
                      lambda: soup.find_all('h2')[0].text, # intro
                      lambda: soup.find_all('td')[12].text.split("：")[1].split(" ")[0]  #author
                      ],
           'ty2016':[ty2016,
                     lambda: url.split('/')[-2], # index in url
                     lambda: str(soup.find_all('p')[1]), # content
                     lambda: soup.find_all('h1')[0].text, # main title
                     lambda: soup.find_all('h1')[0].text, # chapter title
                     lambda: soup.find_all('p')[0].text, # intro
                     lambda: soup.find_all('h2')[1].a.text#author
                     ],
           'dushu369':[dushu369,
                       lambda: url.split('/')[-3], # index in url
                       lambda: str(soup.find_all("td", {"class": "content"})[0]), # content
                       lambda: soup.find_all('td', {'class':'cntitle'})[0].text.split('《')[1][:-1], # main title
                       lambda: soup.find_all('td', {'class':'cntitle'})[0].text, # chapter title
                       lambda: soup.find_all('td', {'class':'Readme'})[0].text, # intro
                       lambda: soup.find_all('td', {'class':'cntitle'})[0].text.split('《')[0]# author
                       ],
           'txshuku':[txshuku,
                      lambda: url.split('/')[-1].split('.')[0], # index in url
                      lambda: str(soup.find_all('div', {"class":"contentbox"})[0]), # content
                      lambda: soup.find_all('h1')[0].text[:-4], # main title
                      lambda: soup.find_all('h1')[0].text, # chapter title
                      lambda: soup.find_all('p')[1].text, # intro
                      # //*[@id="content"]/div/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/p
                      lambda: soup.find_all('p')[1].text# author
                      ],
           'sfacg':[sfacg,
                    lambda: url.split('/')[-3], # index in url
                    lambda: str(soup.find_all('div', {'id':'ChapterBody'})[0]), # content
                    lambda: soup.find_all('h1')[0].text, # main title
                    lambda: soup.find_all('h1')[0].text, # chapter title
                    lambda: soup.find_all('p', {"class": "summary big-profiles"}),  # TODO: intro <- does not work for now
                    lambda: soup.find_all('p', {"class": "summary big-profiles"})# author
                    ]
           }

def get_source_info(url):
    source = ''
    index = ''
    if 'kanunu' in url: # kanunu 1 & 2
        if url.split('/')[-1]:
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
    index = support[source][1]()
    return source, index

def parse_index(soup, source, index, url):
    all_chapter = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if source in support:
            support[source](all_chapter, href, index)
    return all_chapter

# change it the same way as parse index
# /html/body/div[1]/table/tbody/tr/td/table[3]/tbody/tr[3]/td
def get_content(soup, source):

    if source in support:
        content = support[source][2]()

    if source == 'dushu369':
        #TODO: different way to modify br in dushu 369
        content = re.sub('<br/>\n<br/>', '</p>\n<p>', content)
    else:
        content = re.sub('<br/>\n<br/>', '</p>\n<p>', content)
    return content


def get_title_main(soup, source):
    if source in support:
        return support[source][3]()

def get_title_chapter(soup, source):
    if source in support:
        return support[source][4]()


def get_intro(soup, source, url):
    if source != 'sfacg' and source in support:
        return support[source][5]()
    elif source == 'sfacg':
        pos = url.index('MainIndex')
        url = url[:pos]
        # modify url,
        res = requests.get(url)
        # res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        print (soup)
        return support[source][5]()


def get_author(soup, source, url):
    if source != 'txshuku' and source != 'sfacg' and source in support:
        return support[source][6]()
    elif source == 'txshuku':
        indexurl = url.replace('dir','article')
        res = requests.get(indexurl)
        res.encoding = 'gb2312'
        page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
        soup = BeautifulSoup(page, 'html.parser')
        return support[source][6]()

    elif source == 'sfacg':
        pass

# def write_in_md(url):
#     all_chapters = route(url)
#     file = open("test.md","wb")  # The wb indicates that the file is opened for writing in binary mode.
#     for link in all_chapters:
#         res = requests.get(link)
#         res.encoding = 'gb2312'
#         page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
#         soup = BeautifulSoup(page, 'html.parser')
#         title = ('<br/>##' + get_title(soup, get_source(url))).encode('utf-8')
#         content = get_content(soup, get_source(url)).encode('utf-8')
#         file.write(title)
#         file.write(content)
#     file.close()


def get_epub_content(url, folder):
    all_chapters = route(url)
    counter = 1
    header0 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'" \
             " 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns='http://www.w3.org/1999/xhtml'" \
             " xml:lang='zh-CN'>\n<head>\n<title>"
    header1 = "</title>\n<link href='stylesheet.css' type='text/css' rel='stylesheet'/>\n" \
              "<style type='text/css'>@page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style>\n" \
              "</head>\n" \
              "<body>\n"
    h20 = "<h2>\n<span style='border-bottom:1px solid'>"
    h21 = "</span>\n</h2>\n<p>"
    tail = "</p>\n<div class='mbppagebreak'></div></body></html>"
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
    meta_inf_content = "<?xml version='1.0'?>\n<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:" \
                       "container'>\n<rootfiles>\n<rootfile full-path='content.opf' media-type='application/oe" \
                       "bps-package+xml'/>\n</rootfiles>\n</container>"
    os.makedirs(meta_inf_dir, exist_ok=True)
    containxml_path = meta_inf_dir + '/container.xml'
    with open(containxml_path, "w") as f:
        f.write(meta_inf_content)
        f.close()


def catalogxhtml(chapter_dict, title, dirname):
    head1 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN" \
            "' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='" \
            "zh-CN'>\n<head>\n<title>"
    head2 = "</title>\n<link href='stylesheet.css' type='text/css' rel='stylesheet'/><style type='text/css'>\n@page " \
            "{ margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style>\n</head>\n<body>\n<h1>目录<br/>Content</h1>\n<ul>"
    tail = "</ul>\n<div class='mbppagebreak'></div>\n</body>\n</html>"

    list1 = "<li class='catalog'><a href='chapter_"
    list2 = ".xhtml'>"
    list3 = "</a></li>\n"

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
    head1 = "<?xml version='1.0' encoding='utf-8'?>\n\n<package xmlns='http://www.idpf.org/2007/opf' " \
            "xmlns:dc='http://purl.org/dc/elements/1.1/' unique-identifier='bookid' version='2.0'>\n\n " \
            " <metadata xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:opf='http://www.idpf.org/2007/opf'>\n"
    dctitle = "<dc:title>"+title+"</dc:title>\n"
    dccreator = "<dc:creator>"+author+"</dc:creator>\n"
    dcintro = "<dc:description>"+intro+"</dc:description>\n"
    dclanguage = "<dc:language>zh-cn</dc:language>\n"
    dccontributor = "<dc:contributor>" + source_site + ' ' + source_url + "</dc:contributor>\n"
    dcpublisher = "<dc:publisher>"+source_url+"</dc:publisher>\n"
    dcsubject = "<dc:subject>"+source_site+"</dc:subject>\n"
    dcidentifier = "<dc:identifier id='bookid'>pymtrdr:000001</dc:identifier>"
    head2 = "</metadata>\n\n<manifest>"

    content = head1 + dctitle + dccreator + dcintro + dclanguage + dccontributor + dcpublisher + dcsubject + dcidentifier + head2

    item1 = "<item href='chapter_"
    item2 = ".xhtml' id='id"
    item3 = "' media-type='application/xhtml+xml'/>\n"
    idref1 = "<itemref idref='id"
    idref2 = "'/>\n"
    idref = ""

    for chapter, title in chapter_dict.items():
        item = item1 + str(chapter) + item2 + str(chapter) + item3
        content += item
        idref += idref1 + str(chapter) + idref2

    item_other = "<item href='catalog.xhtml' id='catalog' media-type='application/xhtml+xml'/>\n<item href='stylesheet." \
                 "css' id='css' media-type='text/css'/>\n<item href='page.xhtml' id='page' media-type='application/xhtm" \
                 "l+xml'/>\n<item href='toc.ncx' media-type='application/x-dtbncx+xml' id='ncx'/>\n</manifest>"
    spine_head = "<spine toc='ncx'>\n<itemref idref='page'/>\n<itemref idref='catalog'/>\n"
    tail = "<itemref idref='page'/>\n</spine>\n\n<guide>\n<reference href='catalog.xhtml' type='toc' title='目录'/>" \
           "\n</guide>\n</package>"
    content+= item_other + spine_head + idref + tail

    with open(dirname+'/content.opf', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()


def pagexhtml(title, author, intro, source_site, source_url, dirname):
    head1 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'" \
            " 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='" \
            "zh-CN'>\n<head>\n<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>\n<title>书籍信息</title>\n" \
            "<style type='text/css' title='override_css'>\n@page {padding: 0pt; margin:0pt}\nbody { text-align: left;" \
            " padding:0pt; margin: 0pt;font-size: 1.0em}\nul,li{list-style-type:none;margin:0;padding:0;line-height:" \
            " 2.5em;font-size: 0.8em}\ndiv,h1,h2 { margin: 0pt; padding: 0pt}\nh1{font-size:1.2em}\nh2 {font-size: 1.1em}" \
            "\n.copyright{color:#ff4500}\n</style>\n</head>\n<body>\n<div>\n<h1>"
    head2 = "</h1>\n<h2>作者："
    head3 = "</h2>\n<ul>\n<li>内容简介："
    head4 = "</li>\n<li class='copyright'>由 multi_reader 开源项目提供epub下载，现支持将部分中文在线阅读网站的书库直接转成epub格式。\
    \n可访问 https://github.com/RioAraki/multi_reader 查看详情。\n欢迎 fork, star, 提 issue 等。</li>\n<li class='copyright'>书籍内容由"
    head5 = "提供，请访问："
    head6 = "</li>\n</ul>\n</div>\n</body>\n</html>"
    content = head1 + title + head2 + author + head3 + intro + head4 + source_site + head5 + source_url + head6
    with open(dirname+'/page.xhtml', "wb") as f:
        f.write(content.encode('utf-8'))
        f.close()


# TODO: let user modify the format accordingly
def stylesheetcss(dirname):
    content = "body{margin:10px;font-size:1em}ul,li{list-style-type:none;margin:0;padding:0}p{text-indent:2em;line-" \
              "height:1.5em;margin-top:0;margin-bottom:1.5em}.catalog{line-height:2.5em;font-size:.8em}li{border-bot" \
              "tom:1px solid #D5D5D5}h1{font-size:1.6em;font-weight:700}h2{display:block;font-size:1.2em;font-weight" \
              ":700;margin-bottom:.83em;margin-left:0;margin-right:0;margin-top:1em}.mbppagebreak{display:block;marg" \
              "in-bottom:0;margin-left:0;margin-right:0;margin-top:0}a{color:inherit;text-decoration:none;cursor:def" \
              "ault}a[href]{color:blue;text-decoration:none;cursor:pointer}.italic{font-style:italic}"
    with open(dirname+'/stylesheet.css', 'w') as f:
        f.write(content)
        f.close()


# TODO: get more ideas on what meta in head portion does
def tocncx(chapter_dict, title, author, dirname):
    head1 = "<?xml version='1.0' encoding='utf-8'?>\n<ncx xmlns='http://www.daisy.org/z3986/2005/ncx/' version='2005-1'>\n" \
            "<head>\n<meta content='pymtrdr:000001' name='dtb:uid'/>\n<meta content='2' name='dtb:depth'/>\n<meta content='0' name='dtb:totalPageCount'/>\n" \
            "<meta content='0' name='dtb:maxPageNumber'/>\n</head>\n<docTitle>\n<text>"
    head2 = "</text>\n</docTitle>\n\n<docAuthor>\n<text>"
    head3 = "</text>\n</docAuthor>\n\n<navMap>"
    tail = "</navMap>\n\n</ncx>"


    nav1 = "<navPoint id='chapter_"
    nav2 = "' playOrder='"
    nav3 = "'><navLabel><text>"
    nav4 = "</text></navLabel><content src='chapter_"
    nav5 = ".xhtml'/></navPoint>\n"

    content = head1 + title + head2 + author + head3
    for chapter, title in chapter_dict.items():
        content += nav1 +str(chapter)+ nav2 + str(chapter) + nav3 + title + nav4 + str(chapter) + nav5
    content += tail

    with open(dirname+'/toc.ncx', 'wb') as f:
        f.write(content.encode('utf-8'))
        f.close()


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
    # TODO: a better way might be have a META-INF folder ready and copy it to other epub folders since META-INF never changes
    META_INF(dirname)

    # create catelog.xhtml
    catalogxhtml(chapter_dict, title, dirname)

    # create mimetype
    # TODO: a better way might be have a mimetype folder ready and copy it to other epub folders since mimetype never changes
    mimetype(dirname)

    # create content.opf
    source = get_source(url)
    source_site = ""
    source_url = ""
    if 'kanunu' in source:
        source_site = '努努书坊'
        source_url = '[https://www.kanunu8.com/]'
    elif 'ty2016' in source:
        source_site = '天涯书库'
        source_url = '[http://www.ty2016.net/]'
    elif 'dushu369' in source:
        source_site = '读书369'
        source_url = '[http://www.dushu369.com/]'
    contentopf(chapter_dict, title, author, intro, source_site, source_url, dirname)

    # create page.xhtml
    pagexhtml(title, author, intro, source_site, source_url, dirname)

    # create stylesheet.css
    stylesheetcss(dirname)

    # create tocncx
    tocncx(chapter_dict, title, author, dirname)

    return title

if __name__ == "__main__":


    kanunu_index = 'https://www.kanunu8.com/files/yqxs/201103/1863.html'
    kanunu1_index = 'https://www.kanunu8.com/book/4333/'
    kc = 'https://www.kanunu8.com/files/yqxs/201103/1863/43617.html'
    kc1 = 'https://www.kanunu8.com/book/4333/51335.html'

    ty2016_index = 'http://www.ty2016.net/book/Murakami_13/'
    tc = 'http://www.ty2016.net/book/Murakami_13/67710.html'

    dushu369_index = 'http://www.dushu369.com/waiguomingzhu/bngd/'
    dc = 'http://www.dushu369.com/waiguomingzhu/HTML/63294.html'

    txshuku_index = 'http://book.txshuku.net/dir/352.html'
    txc = 'http://book.txshuku.net/chapter/352/29636.html'

    sfacg_index = 'http://book.sfacg.com/Novel/108421/MainIndex/'
    sc = 'http://book.sfacg.com/Novel/108421/183067/1512447/'

    # Test build epub
    # build_epub(kanunu)
    url = txshuku_index
    source, index = get_source_info(url)
    res = requests.get(url)
    res.encoding = 'gb2312'
    page = re.sub('&nbsp;', ' ', res.text)  # for all text in res, change &nbsp to ' '
    soup = BeautifulSoup(page, 'html.parser')

    # content = get_content(soup, source)
    # print (content)
    # title = get_title_main(soup, source)
    # print (title)
    # title = get_title_chapter(soup, source)
    # print(title)
    # print(get_intro(soup, source, url))
    print (get_author(soup, source, url))







