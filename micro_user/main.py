from flask import Flask, request, jsonify
import boto3, requests, os
app = Flask(__name__)

def getDynamo():
    db = boto3.resource('dynamodb')
    return db.Table('groups')

@app.route("/listGroups", methods=['GET', 'POST'])
def listGroups():
    table = getDynamo()
    groupNames = []
    for i in table.scan()["Items"]:
        groupNames.append(i["name"])
    return jsonify(groupNames)

def callDataService(req, path):
    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5001"
    else:
        microServiceURL = "http://data.default.svc.cluster.local"


    resp = requests.post(microServiceURL + path, json = req)
    return resp.json()

    
    # data = request.json
    
    
    # if data["publicAccount"] == "false":
    #     group = authenticate(request.authorization["username"], request.authorization["password"])
    #     if group is None:
    #         return jsonify({"error": "UserUnknown"})
    #     else:
    #         req = {
    #             "public": "false",
    #             "groupName": group["name"],
    #             "action": data["action"]
    #         }
    #         resp = requests.post(microServiceURL, json = req)


def updateMembers(table, members, entry):
    table.update_item(
        Key={
            "name": entry["name"]
        },
        UpdateExpression='SET #val = :val3',
        ExpressionAttributeValues={
            ":val3": members
        },
        ExpressionAttributeNames={
            "#val": "members"
        }
    )


@app.route("/joinGroup", methods=['GET', 'POST'])
def joinGroup():
    data = request.json
    username = data['username']
    password = data['password']
    groupName = data["groupName"]

    db = boto3.resource('dynamodb')
    table = db.Table('groups')

    for i in table.scan()["Items"]:
        if i["name"] == groupName:
            members = i["members"]

            if username + ":" + password in members:
                return jsonify({"response": "Member already in group"}), 400
            else:
                members.append(username + ":" + password)
                updateMembers(table, members, i)
                return jsonify({"response": "User {} was added to the group {}".format(username, groupName)})


@app.route("/leaveGroup", methods=['GET', 'POST'])
def leaveGroup():
    data = request.json
    username = data['username']
    password = data['password']
    groupName = data["groupName"]

    db = boto3.resource('dynamodb')
    table = db.Table('groups')

    for i in table.scan()["Items"]:
        if i["name"] == groupName:
            members = i["members"]

            if username + ":" + password in members:
                members.remove(username + ":" + password)
                updateMembers(table, members, i)

                return jsonify({"response": "User {} was removed from the group {}".format(username, groupName)})

            else:
                return jsonify({"response": "Member not in group"}), 400


@app.route("/addUser", methods=['GET', 'POST'])
def addUser():
        
    cred = request.authorization["username"] + ":" + request.authorization["password"]
    db = boto3.client('dynamodb')

    db = boto3.resource('dynamodb')
    table = db.Table('groups')
    table.put_item(
        Item={
            "name": request.authorization["username"],
            "members": [cred],
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
    db = boto3.resource('dynamodb')
    table = db.Table('groups')
    for group in table.scan()["Items"]:
        if cred in group["members"]:
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