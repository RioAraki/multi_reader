from search import search
from route import build_epub
from compress import compress


name = input("Enter the book name:")
link = search(name)
folder = build_epub(link)
epub = compress(folder)




