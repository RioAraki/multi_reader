# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from django.utils.encoding import escape_uri_path

# test locally, remove the path when test from pypi
import sys
import os
sys.path.append('C:\\Users\\yueli1\\PycharmProjects\\scraper\\epyb')
#

import search as search
import create as create

# sometimes the book_name you typed isnt exactly the name returned by the website: eg: 紫罗兰永恒花园/ 维尔利特·依芙加登
def download(request, file_path, book_name): # do we really need request?
    if os.path.exists(file_path):
        response = HttpResponse(content_type="application/epub+zip")
        print (book_name)
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(book_name)) # more research on why it works
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
        real_name = create.create(book_name)

        print(cwd)
        file_path = os.path.join(cwd, real_name)
        return download(request, file_path, real_name)

    context = {'return_value': book_name,
               'result_1': result,
               'cwd': cwd}

    return HttpResponse(template.render(context, request))
