# How to

## Build docker files



docker build -t docker.io/vladmasarik/htwg-web .
docker push docker.io/vladmasarik/htwg-web

docker build -t docker.io/vladmasarik/htwg-user ./micro-user
docker push docker.io/vladmasarik/htwg-user

docker build -t docker.io/vladmasarik/htwg-data ./micro-data
docker push docker.io/vladmasarik/htwg-data





oc apply -f manifests



## Create secrets
kubectl create secret generic aws-web --from-file=./aws-id --from-file=./aws-pass


## Run all servers


python3 manage.py runserver


FLASK_APP=micro-user/main.py FLASK_DEBUG=1 flask run --debugger


FLASK_APP=micro-data/main.py FLASK_DEBUG=1 flask run -p 5001 --debugger


## Remake the environment

oc delete -f manifests --now && oc create -f manifests && oc get po 
