from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/(?P<pk>\d+)/$', views.home, name='home'),
    url(r'^posts/(?P<pk>\d+)/$', views.post_detail, name='post_detail')
]
