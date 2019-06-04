from flask import Flask, request
import boto3, requests, os, json
app = Flask(__name__)

@app.route("/")
def hello():


    data = request.json()
    gitUser = data["action"]["gitUser"]
    #groupName = data["name"]
    
    if data["public"] == "false":
        db = boto3.resource('dynamodb')
        table = db.Table('groups')
        for i in table.scan()["Items"]:

            # Find the right user
            if i["name"] == groupName:
                dbData = i["data"]
                
                # Which action to performe?
                if data["action"]["label"] == "listRepo":

                    # DB has data?
                    if gitUser in dbData:
                        return dbData[gitUser]["repoList"]
                    else:
                        response = requests.get(('https://api.github.com/users/{}/repos').format(gitUser))
                        repos = json.loads(response.content.decode('utf-8'))

                        # Update DB
                        dbData[gitUser] = {"repoList": repos}
                        table.update_item(
                            Key={
                                "name": i["name"]
                            },
                            UpdateExpression='SET data = :val3',
                            ExpressionAttributeValues={
                                ":val3": dbData
                            }
                        )

                        return dbData[gitUser]["repoList"]
    else:
        response = requests.get(('https://api.github.com/users/{}/repos').format(gitUser))
        repos = json.loads(response.content.decode('utf-8'))

        names = []
        for e in repos:
            names.append(e["name"])
        
        out = {
            "repositories": names
        }
        
        return out

            

    return "Hello World!"