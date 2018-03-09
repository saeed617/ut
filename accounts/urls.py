from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'accounts:login'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate-accounts/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^validate_username/$', views.validate_username, name='validate_username'),
]
