from django.conf.urls import url

from rango import views

app_name = 'rango'
urlpatterns = [
    url(r'^$',
        views.index,
        name='index'),

    url(r'about/$',
        views.about,
        name='about'),
    url(r'^search',
        views.search,
        name='search'),

    # url(r'^register/$',
    #     views.register,
    #     name='register'),

    url(r'^add_category/$',
        views.add_category,
        name='add_category'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page,
        name='add_page'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category,
        name='show_category'),

    # url(r'login/$',
    #     views.user_login,
    #     name='login'),

    url(r'restricted/',
        views.restricted,
        name='restricted'),

    # url(r'logout/$',
    #     views.user_logout,
    #     name='logout'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^goto/$',
        views.track_url,
        name='goto'),

    url(r'^register_profile/$',
        views.register_profile,
        name='register_profile'),

    url(r'^profile/(?P<username>[\w\-]+)/$',
        views.profile,
        name='profile'),

    url(r'^profiles/$',
        views.list_profile,
        name='list_profile'),
    url(r'^like/$',
        views.like_category,
        name='like_category'),
    url(r'^suggest/$',
        views.suggest_category,
        name='suggest_category'),

]
