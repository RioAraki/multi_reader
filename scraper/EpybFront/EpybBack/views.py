from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    book_name = ''
    if request.method == "POST":
        book_name = request.POST.get("book_name")


    context = {'return_value': book_name}

    return HttpResponse(template.render(context, request))
