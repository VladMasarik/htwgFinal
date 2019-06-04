from flask import Flask, request
import boto3, requests, os
app = Flask(__name__)

@app.route("/")
def hello():

    data = request.json()
    
    if data["check"] == "true":
        db = boto3.resource('dynamodb')
        table = db.Table('groups')
        for i in table.scan()["Items"]:
            if (i["name"] == request.authorization["username"] and
                 i["password"] == request.authorization["password"]):
                req = {
                    "valid": "true",
                    "name": i["name"],
                    "action": data["action"]
                }
                response = requests.post(os.environ["DATAURL"], json = req)
                responseData = response.json()
                print(responseData)
                responseData["sessionID"] = i["sessionID"]
                return responseData
        #didnt find user
        return "UserUnknown"

            

    return "Hello World!"