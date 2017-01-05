from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.models import Category, UserProfile
from rango.models import Page


def index(request):
    # context_dict = {'boldmessage': "Crunchy,creamy,cookie,candy,cupcake!"}
    catetory_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': catetory_list, 'pages': pages_list}
    response = render(request, 'rango/index.html', context_dict)
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return response


def track_url(request):
    # page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)


def get_server_side_cookie(request, cookie, default_value=None):
    val = request.session.get(cookie)
    if not val:
        val = default_value
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds >= 5:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = visits
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
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
    visitor_cookie_handler(request)

    context_dict = {'zcl': "copyright:张成龙"}
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)


def search(request):
    pass
    return None


@login_required()
def restricted(request):
    return HttpResponse("Since you're logged in ,you can see this text")


@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('rango:index')
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'rango/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('rango:index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture}
    )

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
    return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def list_profile(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'rango/list_profiles.html', {'userprofile_list': userprofile_list})


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
        if cat_id:
            cat = Category.objects.get(id=int(cat_id))
            if cat:
                likes = cat.likes + 1
                cat.likes = likes
                cat.save()
        return HttpResponse(likes)


def get_category_list(max_result=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__startswith=starts_with)
    else:  # 对原作的修改，如果没有输入过滤条件，则返回全部类别
        cat_list = Category.objects.all()
    if max_result > 0:
        if len(cat_list) > 0:
            cat_list = cat_list[:max_result]
    return cat_list


def suggest_category(request):
    # cat_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cats': cat_list})
