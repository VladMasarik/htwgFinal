from flask import Flask, request, jsonify
import boto3, requests, os, json
app = Flask(__name__)

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

                    return jsonify({"repositories": dbData[gitUser]["repoList"]})
    else:
        response = requests.get(('https://api.github.com/users/{}/repos').format(gitUser))
        repos = json.loads(response.content.decode('utf-8'))

        names = []
        for e in repos:
            names.append(e["name"])
        
        out = {
            "repositories": names
        }
        
        return jsonify(out)

            

    return "Hello World!"