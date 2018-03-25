from search import search_ask
from route import build_epub
from compress import compress


def create():
    link = search_ask()
    folder = build_epub(link)
    epub = compress(folder)

if __name__ == '__main__':
    create()