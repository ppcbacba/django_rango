from django.shortcuts import render

from rango.models import Category
from rango.models import Page


def index(request):
    # context_dict = {'boldmessage': "Crunchy,creamy,cookie,candy,cupcake!"}
    catetory_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': catetory_list, 'pages': pages_list}
    return render(request, 'rango/index.html', context=context_dict)


def show_categoy(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def about(request):
    context_dict = {'zcl': "copyright:张成龙"}
    return render(request, 'rango/about.html', context=context_dict)
