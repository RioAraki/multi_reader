from search import search_ask
from route import build_epub
from compress import compress


def create(book_name):
    if book_name == '':
        book_name = input("Please enter a book's name: ")
    link = search_ask(book_name)
    folder = build_epub(link)
    real_name = compress(folder)
    return real_name

if __name__ == '__main__':
    create(book_name='朝闻道')