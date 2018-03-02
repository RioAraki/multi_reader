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