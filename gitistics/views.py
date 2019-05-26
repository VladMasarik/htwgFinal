from django.shortcuts import render, HttpResponse
import requests
from django.views import View
from .getfromgithub import SearchRepositories, SearchCommits

class IndexView(View):
    
    template_name = 'gitistics/index.html'

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

#Take2
def index(request):
    repository = request.GET.get("repository")
    if repository is None:
        return render(request, 'gitistics/index.html', {'data': None})
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