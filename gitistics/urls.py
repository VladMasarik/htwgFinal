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
    url(r'^api/repoList/$', views.apiRepoList, name='apiRepoList'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^joinGroup/$', views.joinGroup, name='joinGroup'),
    url(r'^leaveGroup/$', views.leaveGroup, name='leaveGroup')
]