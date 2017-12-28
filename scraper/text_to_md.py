import route

kanunu = 'https://www.kanunu8.com/wuxia/201102/1625.html'
kanunu1 = 'https://www.kanunu8.com/book2/10752/'
tianya = 'http://www.ty2016.net/book/Murakami_13/'
lib99 = 'http://www.99lib.net/book/8007/index.htm'


def text_to_txt (url):
    all_chapters = route.route(url)
    for link in all_chapters:


