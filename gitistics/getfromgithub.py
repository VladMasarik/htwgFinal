import json
import requests

class SearchRepositories():
    
    NUMBER_OF_REPOS = 5
    
    def __init__(self, search_term):
        self.search_term = search_term

    def get_from_github(self):
        response = requests.get(('https://api.github.com/search/repositories?q={}').format(self.search_term))
        #get repos from request
        resp_dict = json.loads(response.content.decode('utf-8'))
        #get items only and order by created_at desc
        resp_dict['items'] = sorted(resp_dict['items'], key=lambda x:x['created_at'], reverse=True)
        #slice to NUMBER_OF_REPOS
        repos = resp_dict['items'][:self.NUMBER_OF_REPOS]
        return repos

class SearchCommits():
    
    def __init__(self, repos):
        self.repos = repos

    def get_from_github(self):
        commits = []
        for repo in self.repos:
            response = requests.get(('https://api.github.com/repos/{}/{}/commits').format(repo['owner']['login'],repo['name']))
            #get all commits
            all_commits = json.loads(response.content.decode('utf-8'))
            #slice to one last commmit
            one_commit = all_commits[:1]
            #append to commits
            commits.append(one_commit[0])
        return commits