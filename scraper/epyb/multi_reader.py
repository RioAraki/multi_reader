from search import search_ask
from route import build_epub
from compress import compress


def main():
    link = search_ask()
    folder = build_epub(link)
    epub = compress(folder)




