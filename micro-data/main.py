from flask import Flask, request, jsonify
import boto3, requests, os, json
app = Flask(__name__)



def removeEmptyString(dic):
    for e in dic:
        if isinstance(dic[e], dict):
            dic[e] = removeEmptyString(dic[e])
        if (isinstance(dic[e], str) and dic[e] == ""):
            print("##### Dicrionary:\n", dic, "\n##### Entry:\n", e)
            dic[e] = None
        if isinstance(dic[e], list):
            for entry in dic[e]:
                removeEmptyString(entry)
    return dic
        

@app.route("/", methods=['GET', 'POST'])
def hello():


    data = request.json
    gitUser = data["action"]["gitUser"]
    groupName = data["groupName"]
    
    if data["public"] == "false":
        db = boto3.resource('dynamodb')
        table = db.Table('groups')
        for i in table.scan()["Items"]:

            # Find the right group
            if i["name"] == groupName:
                dbData = i["data"]
                
                # Which action to performe?
                if data["action"]["label"] == "listRepo":

                    # DB has data?
                    if gitUser not in dbData:
                        repos = []
                        page = 1
                        while page > 0:
                            response = requests.get(('https://api.github.com/users/{}/repos?page={}&per_page=100').format(gitUser,page))
                            repoList = response.json()
                            repos = repos + repoList
                            if len(repoList) < 30:
                                page = 0
                            else:
                                page += 1

                        # Update DB
                        dbData[gitUser] = {"repoList": repos}

                        dbData = removeEmptyString(dbData)


                        table.update_item(
                            Key={
                                "name": i["name"]
                            },
                            UpdateExpression='SET #val = :val3',
                            ExpressionAttributeValues={
                                ":val3": dbData
                            },
                            ExpressionAttributeNames={
                                "#val": "data"
                            }
                        )                        

                    return jsonify({"repositories": dbData[gitUser]["repoList"]})
    else:
        response = requests.get(('https://api.github.com/users/{}/repos').format(gitUser))
        # repos = json.loads(response.content.decode('utf-8'))
        repos = response.json()
        
        return jsonify(repos)

            

    return "Hello World!"