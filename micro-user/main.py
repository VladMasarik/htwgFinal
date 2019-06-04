from flask import Flask, request
import boto3, requests, os, json
app = Flask(__name__)

@app.route("/")
def hello():

    data = request.json()
    currentUser = data["action"]["user"]
    groupName = data["name"]
    
    if data["valid"] == "true":
        db = boto3.resource('dynamodb')
        table = db.Table('groups')
        for i in table.scan()["Items"]:

            # Find the right user
            if i["name"] == groupName:
                dbData = i["data"]
                
                # Which action to performe?
                if data["action"]["label"] == "listRepo":

                    # DB has data?
                    if currentUser in dbData:
                        return dbData[currentUser]["repoList"]
                    else:
                        response = requests.get(('https://api.github.com/users/{}/repos').format(currentUser))
                        repos = json.loads(response.content.decode('utf-8'))

                        # Update DB
                        dbData[currentUser] = {"repoList": repos}
                        table.update_item(
                            Key={
                                "name": i["name"]
                            },
                            UpdateExpression='SET data = :val3',
                            ExpressionAttributeValues={
                                ":val3": dbData
                            }
                        )

                        return dbData[currentUser]["repoList"]
    else:
        response = requests.get(('https://api.github.com/users/{}/repos').format(currentUser))
        repos = json.loads(response.content.decode('utf-8'))
        
        return repos

            

    return "Hello World!"