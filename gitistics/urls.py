from django.urls import path

from . import views

app_name = 'gitistics'
urlpatterns = [
    path('', views.index, name='index'),
]