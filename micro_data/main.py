from flask import Flask, request, jsonify
import boto3, requests, os, json, logging
app = Flask(__name__)


def getBucket(bucket):
    s3 = boto3.resource('s3')
    return s3.Object('kittyfolder', bucket)


def getDynamo():
    db = boto3.resource('dynamodb')
    return db.Table('groups')


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
        

def isGroupInBucket(client, groupName):
    """
    Does S3 contain data for the  group X?
    """
    response = client.list_objects(
        Bucket="kittyfolder",
    )
    if "Contents" in response.keys():
        for obj in response['Contents']:
            if obj['Key'] == groupName:
                return True
    return False
    

def putInBucket(obj, data):
    obj.put(Body=data)

def userRepos(gitUser):
    token = os.environ["GITKEY"]
    header = {"Authorization": "token " + token}
    repos = []
    page = 1
    while page > 0:
        response = requests.get(
            'https://api.github.com/users/{}/repos?page={}&per_page=100'.format(gitUser,page),
            headers=header
        )
        repoList = response.json()
        repos = repos + repoList
        if len(repoList) < 30:
            page = 0
        else:
            page += 1
    return repos

def callUserService(body, path):
    microServiceURL = None
    if "HTWGLOCAL" in os.environ:
        microServiceURL = "http://localhost:5000"
    else:
        microServiceURL = "http://user.default.svc.cluster.local"


    resp = requests.post(microServiceURL + path, json = body)
    return resp.json()

def listGroupsForUser(username):
    return callUserService({"username": username}, "/listGroupsPerUser")
    

def get_GitHub_Users_For_User(user):
    """
    For registered user X return all GitHub users that X can access on S3
    """
    s3 = boto3.client("s3")
    response = s3.list_objects(
        Bucket="kittyfolder",
    )
    bucketGroups = []
    if "Contents" in response.keys():
        for obj in response['Contents']:
            bucketGroups.append(obj["Key"])
    userDynamoGroups = listGroupsForUser(user)
    validGroups = list(set(userDynamoGroups) & set(bucketGroups))
    allBody = {}
    for group in validGroups:
        body = s3.get_object(Bucket = "kittyfolder", Key=group)
        body = json.loads(body["Body"].read().decode("utf-8")) 
        allBody = {**allBody, **body} # Merge two dictionaries
    return allBody
    


@app.route("/", methods=['GET', 'POST'])
def root():
    data = request.json
    gitUser = data["action"]["gitUser"]
    
    if data["public"] == "false":
        groupName = data["groupName"]
        user = groupName
        s3 = boto3.client('s3')





        githubUsers = get_GitHub_Users_For_User(user)


        if data["action"]["label"] == "listRepo":

            if gitUser in githubUsers:
                return jsonify({"repositories": githubUsers[gitUser]["repoList"]})
            
            body = s3.get_object(Bucket = "kittyfolder", Key=user)
            body = json.loads(body["Body"].read().decode("utf-8")) 
            body[gitUser] = {"repoList": userRepos(gitUser)}
            s3.put_object(Key=user, Bucket="kittyfolder", Body=json.dumps(body))
            return jsonify({"repositories": body[gitUser]["repoList"]})
            # if gitUser not in groupData:

            #     # No need for empty string since it is a S3 and not Dynamodb anymore?
            #     # dbData = removeEmptyString(groupData)
            #     putInBucket(bucket, groupData)

    else:
        return jsonify({"repositories": userRepos(gitUser)})