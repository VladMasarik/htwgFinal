from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'gitistics'

urlpatterns = [
    path('', views.index, name='index'),
    path('statistics', views.statistics, name='statistics'),
    url(r'^login/$', views.userlogin, name='login'),
    url(r'^logout/$', views.userlogout, name='logout'),
    path('search', views.search, name='search'),
    url(r'^signup/$', views.usersignup, name='signup'),

]