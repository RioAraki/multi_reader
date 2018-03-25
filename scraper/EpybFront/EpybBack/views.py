from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from epyb import search



def index(request):
    template = loader.get_template('index.html')
    book_name = ''
    result = ''
    if request.method == "POST":
        book_name = request.POST.get("book_name")

    if book_name != '':
        result = search.search_ask(book_name)

    context = {'return_value': book_name,
               'result_1': result }

    return HttpResponse(template.render(context, request))
