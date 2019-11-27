from django.shortcuts import render, HttpResponse
import requests, json
from django.views import View


    
NUMBER_OF_REPOS = 5
template_name = 'gitistics/index.html'
    

class Group():
    users = None

class User():
    name = None
    password = None

class Repo():
    name = None




def getTable():
    db = boto3.resource('dynamodb')
    return db.Table('groups')

def getItem(id):
    response = table.get_item(Key={'iddd': int(id)})
    return response['Item']

def upload():
    table.put_item(
                Item={
                    "iddd" : num,
                    'name': form.cleaned_data["name"],
                    'size': form.cleaned_data["size"],
                    'color': form.cleaned_data["color"],
                    'url': image.name,
                }
            )

def getRepositories(repo):
    response = requests.get(('https://api.github.com/search/repositories?q={}').format(repo))
    resp_dict = json.loads(response.content.decode('utf-8'))
    #get items only and order by created_at desc
    resp_dict['items'] = sorted(resp_dict['items'], key=lambda x:x['created_at'], reverse=True)

    repos = resp_dict['items'][:NUMBER_OF_REPOS]
    return repos


def getLastCommit(repo):
    response = requests.get(('https://api.github.com/repos/{}/{}/commits').format(repo['owner']['login'],repo['name']))
    all_commits = json.loads(response.content.decode('utf-8'))
    #slice to one last commmit
    one_commit = all_commits[:1]

    return one_commit[0]


def get(request):
        repository = request.GET.get("repository")
        if repository in ['', None]:
            context = {
                'search_term': repository,
                'data': None,
            }
            return render(request, template_name, context)
        else:
            repos = getRepositories(repository)
            commits = getLastCommit(repos)
            data = zip(repos, commits)
            context = {
                'search_term': repository,
                'data': data,
            }
            return render(request, template_name, context)


#Take2
def index(request):
    repository = request.GET.get("repository")
    if repository is None:
        x = render(request, 'gitistics/index.html', {'data': None})
        x.set_cookie("sess", "kye")
        return x
    userData = requests.get('https://api.github.com/users/{}'.format(repository))

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
    return render(request, 'gitistics/index.html', {'data': userStats})