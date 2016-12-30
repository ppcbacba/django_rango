from django.shortcuts import render

from rango.forms import CategoryForm, PageForm
from rango.models import Category
from rango.models import Page


def index(request):
    # context_dict = {'boldmessage': "Crunchy,creamy,cookie,candy,cupcake!"}
    catetory_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': catetory_list, 'pages': pages_list}
    return render(request, 'rango/index.html', context=context_dict)


def show_categories(request):
    context_dict = {}
    categories = Category.objects.all()
    context_dict['categories'] = categories
    return render(request, 'rango/show_categories.html', context_dict)
def show_category(request, category_name_slug):
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


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExit:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid:
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def about(request):
    context_dict = {'zcl': "copyright:张成龙"}
    return render(request, 'rango/about.html', context=context_dict)
