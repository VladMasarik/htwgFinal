from flask import Flask, request
import boto3, requests, os
app = Flask(__name__)

@app.route("/")
def userService():

    data = request.json()
    
    if data["publicAccount"] == "false":
        db = boto3.resource('dynamodb')
        table = db.Table('groups')
        for i in table.scan()["Items"]:
            if (i["name"] == request.authorization["username"] and
                 i["password"] == request.authorization["password"]):
                req = {
                    "public": "false",
                    "name": i["name"],
                    "action": data["action"]
                }
                return requests.post("data.default.svc.cluster.local", json = req)
        #didnt find user
        return "UserUnknown"
    else:
        req = {
                    "public": "true",
                    "action": data["action"]
                }
        return requests.post("data.default.svc.cluster.local", json = req)

            

    return "Hello World!"