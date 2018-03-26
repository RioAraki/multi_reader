from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
import epyb
import os

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise False

def index(request):
    template = loader.get_template('index.html')
    book_name = ''
    result = ''
    if request.method == "POST":
        book_name = request.POST.get("book_name")

    if book_name != '':
        result = epyb.search.search_ask(book_name)
        epyb.create()

    cwd = os.getcwd()
    context = {'return_value': book_name,
               'result_1': result,
               'cwd': cwd}




    return HttpResponse(template.render(context, request))
