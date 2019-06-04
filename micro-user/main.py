from flask import Flask, request, jsonify
import boto3, requests, os
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def userService():
    microServiceURL = None
    if os.environ["HTWGLOCAL"] == "true":
        microServiceURL = "http://localhost:5001"
    else:
        microServiceURL = "http://data.default.svc.cluster.local"
    data = request.json
    print(data)
    
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

        
        # data.default.svc.cluster.local
        resp = requests.post(microServiceURL, json = req)
        jas = resp.json()
        return jsonify(jas)

            

    return "Hello World!"