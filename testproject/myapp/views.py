from django.shortcuts import render, HttpResponse

# Create your views here.

def hello(request, id):
    return HttpResponse('Hello World Id=' + str(id))

def article(request, year, slug):
    result = 'The aeticle page'
    return HttpResponse(str(year) + str(slug))

def index(request):
    return render(request, 'index.html')
