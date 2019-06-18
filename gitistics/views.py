from django.shortcuts import render, HttpResponse
import requests, json, os
from django.views import View
from .getfromgithub import SearchRepositories, SearchCommits
from django.http import JsonResponse

from gitistics.forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def index(request):
    username = request.COOKIES.get('username')
    password = request.COOKIES.get('password')
    if authenticate(username, password):
        cont = {
            "user": {
                "logged" : "true",
                "username": username
            }
        } 
        return render(request, 'gitistics/index.html', context=cont)
    return render(request, 'gitistics/index.html')

def userlogout(request):
    resp = HttpResponseRedirect("/")
    resp.delete_cookie("username")
    resp.delete_cookie("password")
    return resp


def addUser(username, password):
    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5000"
    else:
        microServiceURL = "http://user.default.svc.cluster.local"

    resp = requests.post(microServiceURL + "/addUser", auth=(username, password) , json = {})
    return resp

def authenticate(username, password):
    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5000"
    else:
        microServiceURL = "http://user.default.svc.cluster.local"
    resp = requests.post(microServiceURL + "/userauth", auth=(username, password) , json = {})
    
    return resp.json()["response"] == "true"

def usersignup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            addUser(user_form.cleaned_data["username"], user_form.cleaned_data["password"])
            resp = HttpResponseRedirect("/")
            resp.set_cookie("username", user_form.cleaned_data["username"])
            resp.set_cookie("password", user_form.cleaned_data["password"])
            return resp
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'gitistics/signup.html', {'user_form':user_form, 'registered':registered})

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username, password)
        if user:
            resp = HttpResponseRedirect("/")
            resp.set_cookie("username", username)
            resp.set_cookie("password", password)
            return resp
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


def collectData(action, auth = None):

    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5000"
    else:
        microServiceURL = "http://user.default.svc.cluster.local"

    req = {
        "action": action
    }

    if auth is None or auth["user"] is None:
        auth = {
            "user": "public",
            "pass": "none"
        }
        req["publicAccount"] = "true"
    else:
        req["publicAccount"] = "false"

    response = requests.post(microServiceURL, auth=(auth["user"], auth["pass"]) , json = req)
    resp = response.json()

    names = []
    for e in resp:
        names.append(e["name"])   

    return names
    
def apiRepoList(request):
    repo = request.GET.get("search_term")
    username = request.COOKIES.get("username")
    password = request.COOKIES.get("password")
    auth = {
        "user": username,
        "pass": password
    }
    action = {
        "label": "listRepo",
        "gitUser": repo,
    }
    
    if repo is not None:

        ctx = {
        'list': collectData(action, auth)
        }
        return JsonResponse(ctx)
    return JsonResponse({"list": ["one","two","three"]})

def search(request):
    repo = request.GET.get("search_term")
    username = request.COOKIES.get("username")
    password = request.COOKIES.get("password")
    auth = {
        "user": username,
        "pass": password
    }
    action = {
        "label": "listRepo",
        "gitUser": repo,
    }
    

    

    if repo is not None:

        userData = requests.get('https://api.github.com/users/{}'.format(repo))
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

        # Get a list of dictionaries full of languages
        repos = []
        for e in collectData(action, auth):
            response = requests.get(('https://api.github.com/repos/{}/{}/languages').format(repo,e))
            repoList = response.json()
            repos.append(repoList)
        # END

        ctx = {
        'data': userStats,
        'repoList': collectData(action, auth)
        }
        return render(request, 'gitistics/search.html', context=ctx)

    return render(request, 'gitistics/search.html')