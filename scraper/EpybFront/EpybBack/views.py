from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader

# test locally, remove the path when test from pypi
import sys
import os
sys.path.append('C:\\Users\\yueli1\\PycharmProjects\\scraper\\epyb')
print (os.getcwd())
#

import search as search
import create as create


def download(request, file_path, book_name): # do we really need request?
    if os.path.exists(file_path):
        response = HttpResponse(content_type="application/epub+zip")
        response['X-Sendfile'] = file_path
        response['Content-Disposition'] = 'attachment; filename=abc.epub'
        print (response)
        return response
    raise False

def index(request):
    template = loader.get_template('index.html')
    book_name = ''
    result = ''
    if request.method == "POST":
        book_name = request.POST.get("book_name")
    cwd = os.getcwd()
    if book_name != '':
        result = search.search_ask(book_name)
        create.create(book_name)

        print(cwd)
        file_path = os.path.join(cwd, book_name) + '.epub'
        download(request, file_path, book_name)

    context = {'return_value': book_name,
               'result_1': result,
               'cwd': cwd}

    return HttpResponse(template.render(context, request))
