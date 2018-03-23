content_header_0 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n" \
                   "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'"" 'http:" \
                   "//www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns=" \
                   "'http://www.w3.org/1999/xhtml'" \
                   " xml:lang='zh-CN'>\n<head>\n<title>"
content_header_1 = "</title>\n<link href='stylesheet.css' type='text/css' rel='stylesheet'/>\n" \
                   "<style type='text/css'>@page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style>\n" \
                   "</head>\n" \
                   "<body>\n"
h20 = "<h2>\n<span style='border-bottom:1px solid'>"
h21 = "</span>\n</h2>\n<p>"
tail = "</p>\n<div class='mbppagebreak'></div></body></html>"
meta_inf_content = "<?xml version='1.0'?>\n<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:" \
                       "container'>\n<rootfiles>\n<rootfile full-path='content.opf' media-type='application/oe" \
                       "bps-package+xml'/>\n</rootfiles>\n</container>"
cat_h1 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN" \
            "' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='" \
            "zh-CN'>\n<head>\n<title>"
cat_h2 = "</title>\n<link href='stylesheet.css' type='text/css' rel='stylesheet'/><style type='text/css'>\n@page " \
            "{ margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style>\n</head>\n<body>\n<h1>目录<br/>Content</h1>\n<ul>"
cat_tail = "</ul>\n<div class='mbppagebreak'></div>\n</body>\n</html>"
cat_list1 = "<li class='catalog'><a href='chapter_"
cat_list2 = ".xhtml'>"
cat_list3 = "</a></li>\n"
opf_h1 = "<?xml version='1.0' encoding='utf-8'?>\n\n<package xmlns='http://www.idpf.org/2007/opf' " \
            "xmlns:dc='http://purl.org/dc/elements/1.1/' unique-identifier='bookid' version='2.0'>\n\n " \
            " <metadata xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:opf='http://www.idpf.org/2007/opf'>\n"
opf_h2 = "</metadata>\n\n<manifest>"
opf_i1 = "<item href='chapter_"
opf_i2 = ".xhtml' id='id"
opf_i3 = "' media-type='application/xhtml+xml'/>\n"
opf_id1 = "<itemref idref='id"
opf_id2 = "'/>\n"
opf_id = ""
opf_io = "<item href='catalog.xhtml' id='catalog' media-type='application/xhtml+xml'/>\n<item href='stylesheet." \
                 "css' id='css' media-type='text/css'/>\n<item href='page.xhtml' id='page' media-type='application/xhtm" \
                 "l+xml'/>\n<item href='toc.ncx' media-type='application/x-dtbncx+xml' id='ncx'/>\n</manifest>"

opf_sh = "<spine toc='ncx'>\n<itemref idref='page'/>\n<itemref idref='catalog'/>\n"
opf_tail = "<itemref idref='page'/>\n</spine>\n\n<guide>\n<reference href='catalog.xhtml' type='toc' title='目录'/>" \
           "\n</guide>\n</package>"

px_h1 = "<?xml version='1.0' encoding='utf-8' standalone='no'?>\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'" \
            " 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='" \
            "zh-CN'>\n<head>\n<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>\n<title>书籍信息</title>\n" \
            "<style type='text/css' title='override_css'>\n@page {padding: 0pt; margin:0pt}\nbody { text-align: left;" \
            " padding:0pt; margin: 0pt;font-size: 1.0em}\nul,li{list-style-type:none;margin:0;padding:0;line-height:" \
            " 2.5em;font-size: 0.8em}\ndiv,h1,h2 { margin: 0pt; padding: 0pt}\nh1{font-size:1.2em}\nh2 {font-size: 1.1em}" \
            "\n.copyright{color:#ff4500}\n</style>\n</head>\n<body>\n<div>\n<h1>"
px_h2 = "</h1>\n<h2>作者："
px_h3 = "</h2>\n<ul>\n<li>内容简介："
px_h4 ="</li>\n<li class='copyright'>由 epyb 开源项目提供 epub 下载，现支持将部分中文在线阅读网站的书库直接转成 epub 格式。\
    \n可访问 https://github.com/RioAraki/multi_reader 查看详情。\n欢迎 fork, star, 提 issue 等。</li>\n<li class='copyright'>书籍内容由"
px_h5 = "提供，请访问："
px_h6 = "</li>\n</ul>\n</div>\n</body>\n</html>"
style_c = "body{margin:10px;font-size:1em}ul,li{list-style-type:none;margin:0;padding:0}p{text-indent:2em;line-" \
              "height:1.5em;margin-top:0;margin-bottom:1.5em}.catalog{line-height:2.5em;font-size:.8em}li{border-bot" \
              "tom:1px solid #D5D5D5}h1{font-size:1.6em;font-weight:700}h2{display:block;font-size:1.2em;font-weight" \
              ":700;margin-bottom:.83em;margin-left:0;margin-right:0;margin-top:1em}.mbppagebreak{display:block;marg" \
              "in-bottom:0;margin-left:0;margin-right:0;margin-top:0}a{color:inherit;text-decoration:none;cursor:def" \
              "ault}a[href]{color:blue;text-decoration:none;cursor:pointer}.italic{font-style:italic}"
toc_h1 = "<?xml version='1.0' encoding='utf-8'?>\n<ncx xmlns='http://www.daisy.org/z3986/2005/ncx/' version='2005-1'>\n" \
            "<head>\n<meta content='pymtrdr:000001' name='dtb:uid'/>\n<meta content='2' name='dtb:depth'/>\n<meta content='0' name='dtb:totalPageCount'/>\n" \
            "<meta content='0' name='dtb:maxPageNumber'/>\n</head>\n<docTitle>\n<text>"
toc_h2 = "</text>\n</docTitle>\n\n<docAuthor>\n<text>"
toc_h3 = "</text>\n</docAuthor>\n\n<navMap>"
toc_t = "</navMap>\n\n</ncx>"
toc_n1 = "<navPoint id='chapter_"
toc_n2 = "' playOrder='"
toc_n3 = "'><navLabel><text>"
toc_n4 = "</text></navLabel><content src='chapter_"
toc_n5 = ".xhtml'/></navPoint>\n"

