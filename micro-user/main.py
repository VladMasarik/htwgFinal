from flask import Flask, request, jsonify
import boto3, requests, os
app = Flask(__name__)


@app.route("/addUser", methods=['GET', 'POST'])
def addUser():
        
    cred = request.authorization["username"] + ":" + request.authorization["password"]
    db = boto3.client('dynamodb')
    x = db.list_tables()

    db = boto3.resource('dynamodb')
    table = db.Table('groups')
    table.put_item(
        Item={
            "name": request.authorization["username"],
            "groupUsers": [cred],
            "data": {}
        }
    )

    return jsonify({"result": "true"})




def authenticate(username, password):
    cred = username + ":" + password
    db = boto3.resource('dynamodb')
    table = db.Table('groups')
    for group in table.scan()["Items"]:
        if cred in group["groupUsers"]:
            return group
    return None
    



@app.route("/", methods=['GET', 'POST'])
def userService():
    microServiceURL = None
    if os.environ["HTWGLOCAL"] == "true":
        microServiceURL = "http://localhost:5001"
    else:
        microServiceURL = "http://data.default.svc.cluster.local"
    data = request.json
    
    
    if data["publicAccount"] == "false":
        group = authenticate(request.authorization["username"], request.authorization["password"])
        if group in None:
            return jsonify({"error": "UserUnknown"})
        else:
            req = {
                "public": "false",
                "groupName": group["name"],
                "action": data["action"]
            }
            return requests.post(microServiceURL, json = req)
    else:
        req = {
            "public": "true",
            "action": data["action"]
        }

        resp = requests.post(microServiceURL, json = req)
        return jsonify(resp.json())

            

    return "Hello World!"