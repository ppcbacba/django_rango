from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category
from rango.models import Page


def index(request):
    # context_dict = {'boldmessage': "Crunchy,creamy,cookie,candy,cupcake!"}
    catetory_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': catetory_list, 'pages': pages_list}
    return render(request, 'rango/index.html', context=context_dict)


# def show_categories(request):
#     context_dict = {}
#     categories = Category.objects.all()
#     context_dict['categories'] = categories
#     return render(request, 'rango/show_categories.html', context_dict)
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


def register(request):
    # A boolean value for telling  the template
    # whether the registration was successful
    # Set to False initiallly.Code changes value to
    # True when registion succeeds.
    registered = False

    # If it's a HTTP POST,we're intrested in processing form data
    if request.method == 'POST':
        # Attemp to grab information from the raw form information
        # Note that we make user of both UserForm and UserPofileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password withd the set_password method
            # Once hased ,we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the Userprofile instance
            # Since we need to set the user attribute ourselves,
            # we set commit=False . This delays saving the model
            # until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # if so,we need to get it from the input form and
            # put it in the UserPorfile model
            if 'picutre' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to indicate that template
            # registration wes successful
            register = True
        else:
            # Invalid form or forms -mistakes or something else?
            # Print problems to the terminal
            print(user_form.errors, profile_form.errors)

    else:
        # Not a Http post,so we render our form using two ModelForm instance
        # These form will be blank,ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending ot the context
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    # If the request is a Http post,try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user
        # This information is obtained from the login form
        # We use request POST get('，variable') as opposed
        # to request POST('<variable>'),because the
        # request.POST.get('<variable>')returns None if the
        # value does not exit,while request.POST['variable']
        # will raise a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid -a User object is returned if it is
        user = authenticate(username=username, password=password)

        # If we have a User object ,the details are correct
        # If None,no user with matching credentials was found

        if user:
            # Is the account active?It could have been disabled
            if user.is_active:
                # If the account is valid and active,we can log the user in
                # We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                # An inactive account was used --no logging in!
                return HttpResponse("Your Rango account is disable")
        else:
            # Bad login details
            print("Invalid login details: ", username, password)
            return HttpResponse("Invalid login details supplied")

            # The request is not a HTTP POST,so display the login form
            # This scenario would most likely be a HTTP GET
    else:
        return render(request, 'rango/login.html', {})
