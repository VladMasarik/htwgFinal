from flask import Flask, request, jsonify
import boto3, requests, os, json
app = Flask(__name__)


def getBucket(bucket):
    s3 = boto3.resource('s3')
    return s3.Object('kittyfolder', bucket)


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

def updateMembers(table, members):
    table.update_item(
        Key={
            "name": i["name"]
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
    groupName = data["groupName"]

    db = boto3.resource('dynamodb')
    table = db.Table('groups')

    for i in table.scan()["Items"]:
        if i["name"] == groupName:
            members = i["members"]

            if username in members:
                return "Member already in group", 400
            else:
                members.append(username)
                updateMembers(table, members)
                return jsonify({"result": "User {} was added to the group {}".format(username, groupName)})


@app.route("/leaveGroup", methods=['GET', 'POST'])
def leaveGroup():
    data = request.json
    username = data['username']
    groupName = data["groupName"]

    db = boto3.resource('dynamodb')
    table = db.Table('groups')

    for i in table.scan()["Items"]:
        if i["name"] == groupName:
            members = i["members"]

            if username in members:
                members.remove(username)
                updateMembers(table, members)

                return jsonify({"result": "User {} was removed from the group {}".format(username, groupName)})

            else:
                return "Member not in group", 400


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
        

def getBuckerJSON(obj):
    body = obj.get()['Body'].read()
    body = body.decode('utf-8') 
    return json.loads(body)

def putInBucket(obj, data):
    obj.put(Body=data)

def userRepos(gitUser):
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
    return repos



@app.route("/", methods=['GET', 'POST'])
def hello():

    data = request.json
    gitUser = data["action"]["gitUser"]
    
    if data["public"] == "false":
        groupName = data["groupName"]
        s3 = boto3.resource('s3')
        bucket = s3.Object('kittyfolder', groupName)

        groupData = getBuckerJSON(bucket)

        if data["action"]["label"] == "listRepo":

            if gitUser not in groupData:
                groupData[gitUser] = {"repoList": userRepos(gitUser)}

                # No need for empty string since it is a S3 and not Dynamodb anymore?
                # dbData = removeEmptyString(groupData)
                putInBucket(bucket, groupData)                   

            return jsonify({"repositories": groupData[gitUser]["repoList"]})
    else:
        response = requests.get(('https://api.github.com/users/{}/repos').format(gitUser))
        repos = response.json()
        
        return jsonify(repos)