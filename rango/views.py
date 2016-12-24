from django.shortcuts import render


def index(request):
    context_dict = {'boldmessage': "Crunchy,creamy,cookie,candy,cupcake!"}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'zcl': "copyright:张成龙"}
    return render(request, 'rango/about.html', context=context_dict)
