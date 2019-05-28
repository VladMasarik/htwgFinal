from django.urls import path

from . import views

app_name = 'gitistics'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('statistics', views.statistics, name='statistics'),
    #path('search', views.search, name='search'),
    path('', views.SearchView.as_view(), name='search'),
]