# Create your views here.
from django.shortcuts import render, HttpResponse
import requests
from django.views import View
from .getfromgithub import SearchRepositories, SearchCommits

from gitistics.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'gitistics/index.html')
'''
def login(request):
    return render(request, 'gitistics/login.html')

def signup(request):
    return render(request, 'gitistics/signup.html')
'''

@login_required
def special(request):
    return HttpResponse("You are logged in!")

@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('gitistics/index'))

def usersignup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'gitistics/signup.html', {'user_form':user_form, 'registered':registered})

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('gitistics/index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given.")
    else:
        return render(request, 'gitistics/login.html', {})

def statistics(request):
    userData = requests.get('https://api.github.com/users/VladMasarik')
    dataList = []
    dataList.append(userData.json())
    cleanedData = []
    userStats = {}
    for data in dataList:
        userStats['name'] = data['name']
        userStats['email'] = data['email']
        userStats['public_repos'] = data['public_repos']
        userStats['avatar_url'] = data['avatar_url']
        userStats['followers'] = data['followers']
        userStats['following'] = data['following']
        userStats['location'] = data['location']
        userStats['created_at'] = data['created_at']
        userStats['updated_at'] = data['updated_at']
    cleanedData.append(userStats)

    return render(request, 'gitistics/statistics.html', {'data': userStats})

'''
def search(request):
    return render(request, 'gitistics/search.html')
'''

class SearchView(View):
    
    template_name = 'gitistics/search.html'

    def get(self, request, *args, **kwargs):
        search_term = self.request.GET.get('search_term', None)
        if search_term == '':
            context = {
                'search_term': search_term,
                'data': None,
            }
            return render(request, self.template_name, context)
        else:
            repos = SearchRepositories(search_term).get_from_github()
            commits = SearchCommits(repos).get_from_github()
            data = zip(repos, commits)
            context = {
                'search_term': search_term,
                'data': data,
            }
            return render(request, self.template_name, context)