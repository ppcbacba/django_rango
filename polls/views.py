from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello,world,Your at the polls index")
