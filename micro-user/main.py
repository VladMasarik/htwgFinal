from flask import Flask, request, jsonify
import boto3, requests, os
app = Flask(__name__)


@app.route("/addUser", methods=['GET', 'POST'])
def addUser():
        
    cred = request.authorization["username"] + ":" + request.authorization["password"]
    db = boto3.client('s3')

    db = boto3.resource('s3')
    table = db.Table('groups')
    table.put_item(
        Item={
            "name": request.authorization["username"],
            "groupUsers": [cred],
            "data": {}
        }
    )

    return jsonify({"result": "true"})



@app.route("/userauth", methods=['GET', 'POST'])
def urlUserAuthenticate():
    group = authenticate(request.authorization["username"], request.authorization["password"])

    if group is None:
        return jsonify({"response": "false"})
    else:
        return jsonify({"response": "true"})


def authenticate(username, password):
    cred = username + ":" + password
    db = boto3.resource('s3')
    table = db.Table('groups')
    for group in table.scan()["Items"]:
        if cred in group["groupUsers"]:
            return group
    return None
    



@app.route("/", methods=['GET', 'POST'])
def userService():
    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5001"
    else:
        microServiceURL = "http://data.default.svc.cluster.local"
    data = request.json
    
    
    if data["publicAccount"] == "false":
        group = authenticate(request.authorization["username"], request.authorization["password"])
        if group is None:
            return jsonify({"error": "UserUnknown"})
        else:
            req = {
                "public": "false",
                "groupName": group["name"],
                "action": data["action"]
            }
            resp = requests.post(microServiceURL, json = req)
            return jsonify(resp.json())
    else:
        req = {
            "public": "true",
            "action": data["action"]
        }

        resp = requests.post(microServiceURL, json = req)
        return jsonify(resp.json())

            

    return "Hello World!"