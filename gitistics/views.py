import requests, json, os
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib.auth import login
from django.views import View
from django.urls import reverse
from gitistics.forms import UserForm

def index(request):
    username, _ = authenticate(request)
    if username is not None:
        cont = {
            "user": {
                "logged" : "true",
                "username": username,
            ### lenght ? for number of registerd users -> end of index.html 
            "groupList": callUserService({}, "/listGroups")
            }
        } 
        return render(request, 'gitistics/index.html', context=cont)
    return render(request, 'gitistics/index.html')

def userlogout(request):
    resp = HttpResponseRedirect("/")
    resp.delete_cookie("username")
    resp.delete_cookie("password")
    return resp

def joinGroup(request):
    username, password = authenticate(request)
    body = {
        "username": username,
        "password": password,
        "groupName": request.GET.get("group")
    }
    callUserService(body, "/joinGroup")
    return HttpResponseRedirect("/profile")

def leaveGroup(request):
    username, password = authenticate(request)
    body = {
        "username": username,
        "password": password,
        "groupName": request.GET.get("group")
    }
    callUserService(body, "/leaveGroup")
    return HttpResponseRedirect("/profile")

def callUserService(data, path):
    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5000"
    else:
        microServiceURL = "http://user.default.svc.cluster.local"
    resp = requests.post(microServiceURL + path, json = data)
    
    return resp.json()

def parsePOSTRequestBody(request):
    body = request.read().decode("utf-8")
    body = body.split("&")
    result = {}
    for parameter in body:
        parameter = parameter.split("=")
        result[parameter[0]] = parameter[1]
    return result

def profile(request):
    username, password = authenticate(request)

    if username is not None:
        # /joinGroup?group{{group}}">join</p><p href="/leaveGroup?group{{group}}
        ctx = {
            "groupList": callUserService({}, "/listGroups")
        }
        
        return render(request, "gitistics/profile.html", context=ctx)
    
    return HttpResponseRedirect("/")

def addUser(username, password):
    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5000"
    else:
        microServiceURL = "http://user.default.svc.cluster.local"

    resp = requests.post(microServiceURL + "/addUser", auth=(username, password) , json = {})
    return resp

def authenticate(request = None, username = None, password = None):
    if request is not None:
        username = request.COOKIES.get("username")
        password = request.COOKIES.get("password")

    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5000"
    else:
        microServiceURL = "http://user.default.svc.cluster.local"

    resp = requests.post(microServiceURL + "/userauth", auth=(username, password) , json = {})

    if resp.json()["response"] == "true":
        return username, password
    else:
        return None, None

def usersignup(request):
    registered = False
    if request.method == 'POST':
        
        details = parsePOSTRequestBody(request)
        addUser(details["username"], details["password"])
        resp = HttpResponseRedirect("/")
        resp.set_cookie("username", details["username"])
        resp.set_cookie("password", details["password"])
        return resp
    return render(request,'gitistics/signup.html', {'registered':registered})

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user, _ = authenticate(None, username, password)
        if user is not None:
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

########### todo
def statistics(request):
    token = "e75afd5f63d505a78237cfa3b3169d9256824a16"
    header = {"Authorization": "token " + token}
    userData = requests.get('https://api.github.com/users/VladMasarik', headers=header)
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
########### todo

def collectData(action, auth = None):
    """
    Returns list of repositories.
    """
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
    for e in resp["repositories"]:
        names.append(e["name"])   

    return names

def apiGithubUserLanguages(request):
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

    repos = []
    langtoken = os.environ["GITKEY"]
    langheader = {"Authorization": "token " + langtoken}
    for e in collectData(action, auth):
        langData = requests.get(
            'https://api.github.com/repos/{}/{}/languages'.format(repo,e),
            headers=langheader
        ) 
        repoList = langData.json()
        repos.append(repoList)

    out = {}
    for listEntry in repos:
        for key in listEntry:
            if key in out.keys():
                out[key] += listEntry[key]
            else:
                out[key] = listEntry[key]

    all = 0
    for key in out:
        all += out[key]
    for key in out:
        out[key] = ((out[key] * 10000) // all) / 100 # Real number representing percentage in form 3.32
    return out # Dictionary with a language and a percentage
 
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
        token = os.environ["GITKEY"]
        header = {"Authorization": "token " + token}
        userData = requests.get(
            'https://api.github.com/users/{}'.format(repo),
            headers=header
        ) 
        dataList = []
        dataList.append(userData.json())
        cleanedData = []
        userStats = {}
        for data in dataList:
            userStats['name'] = data['name']
            userStats['public_repos'] = data['public_repos']
            userStats['avatar_url'] = data['avatar_url']
            userStats['followers'] = data['followers']
            userStats['following'] = data['following']
            userStats['created_at'] = data['created_at']
        cleanedData.append(userStats)

        ctx = {
        'data': userStats,
        'repoList': collectData(action, auth),
        'langsList': apiGithubUserLanguages(request)
        }
        return render(request, 'gitistics/search.html', context=ctx)

    return render(request, 'gitistics/search.html')