from django.http import HttpResponse
def index(request):
    return HttpResponse("Rango says hello world<br /><a href='rango/about/'>about</a>")

def about(request):
    return HttpResponse("Rango says this is about page<br /><a href='/rango/'>home</a>")
