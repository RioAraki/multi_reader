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
    head4 = "</li>\n<li class='copyright'>由 multi_reader 开源项目提供epub下载，可访问 https://github.com/" \
            "RioAraki/multi_reader 查看详情\n欢迎 fork, star, 提issue 等。</li>\n<li class='copyright'>书籍内容由"
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


if __name__ == "__main__":

    kanunu = 'https://www.kanunu8.com/wuxia/201102/1625.html'
    kanunu1 = 'https://www.kanunu8.com/book2/10752/'
    kanunu1_1 = 'https://www.kanunu8.com/book2/10741/'
    ty2016 = 'http://www.ty2016.net/book/Murakami_13/'
    lib99 = 'http://www.99lib.net/book/8007/index.htm'

    # Test build epub
    build_epub(kanunu)












