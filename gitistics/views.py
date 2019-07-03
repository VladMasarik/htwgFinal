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
            },
            ### lenght ? for number of registerd users -> end of index.html 
            "groupList": callUserService({}, "/listGroups")
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
    """
    Call service and return its body as JSON
    """
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
    username, _ = authenticate(request)

    if username is not None:
        # /joinGroup?group{{group}}">join</p><p href="/leaveGroup?group{{group}}
        resp = callUserService({"user": username}, "/userDetail")
        ctx = {
            'user': username,
            "groupList": callUserService({}, "/listGroups"),
            "billing": {
                "reads": resp["reads"],
                "writes": resp["writes"],
                "amount": resp["reads"] * 2 + resp["writes"] * 8
            }
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

def collectData(action, auth = None):
    """ Returns list of repositories. """
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

def collectResps(action, auth = None):
    """ Returns repositories. """
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

    return resp

def callUserService2(action, auth = None):
    """ Returns list of repositories. """
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
    response = response.json()
    return response["repositories"]

def apiGithubUserLanguages(request):
    """ Returns dictionary of languages and percentages. """
    repo = request.GET.get("search_term")
    username, password = authenticate(request)
    auth = {
        "user": username,
        "pass": password
    }
    action = {
        "label": "listLanguages",
        "gitUser": repo,
    }
    out = callUserService2(action, auth)



    ctx = {
       "languageList": out
    }
    return JsonResponse(ctx)

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
        'list': collectResps(action, auth)
        }
        return JsonResponse(ctx)
    return JsonResponse({"list": ["one","two","three"]})

def apiGroupUserList(request):
    ctx = {
       "groupList": callUserService({}, "/listGroups")
    }
    return JsonResponse(ctx)

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

    SecondAction = {
        "label": "detailUser",
        "gitUser": repo,
    }
    
    if repo is not None:
        token = os.environ["GITKEY"]
        header = {"Authorization": "token " + token}
        userData = requests.get(
            'https://api.github.com/users/{}'.format(repo),
            headers=header
        ) 

        ctx = {
        'user': username,
        'data': userData.json()
        }
        return render(request, 'gitistics/search.html', context=ctx)

    return render(request, 'gitistics/search.html')