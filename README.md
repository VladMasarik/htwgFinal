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

Before set the environment variable `HTWGLOCAL` to `true`.
`vi ~/.profile` and write at the end 

```
export HTWGLOCAL=true
export AWS_DEFAULT_REGION=us-west-2
```


python3 manage.py runserver


FLASK_APP=micro-user/main.py flask run --port 5000


FLASK_APP=micro-data/main.py flask run --port 5001


## Remake the environment

oc delete -f manifests --now && oc create -f manifests && oc get po 
