# How to

## Build docker files


docker build -t docker.io/vladmasarik/htwg-web .
docker push docker.io/vladmasarik/htwg-web

docker build -t docker.io/vladmasarik/htwg-user ./micro_user
docker push docker.io/vladmasarik/htwg-user

docker build -t docker.io/vladmasarik/htwg-data ./micro_data
docker push docker.io/vladmasarik/htwg-data





oc apply -f manifests



## Create secrets
kubectl create secret generic aws-web \
 --from-file=/home/vmasarik/projects/htwgFinal/aws-id \
 --from-file=/home/vmasarik/projects/htwgFinal/aws-pass \
 --from-file=/home/vmasarik/projects/htwgFinal/gitkey


## Run all servers

Before set the environment variable `HTWGLOCAL` to `true`.
`vi ~/.profile` and write at the end 

```
export HTWGLOCAL=true
export AWS_DEFAULT_REGION=us-west-2
```


python3 manage.py runserver


FLASK_APP=micro_user/main.py FLASK_DEBUG=1 flask run --port 5000


FLASK_APP=micro_data/main.py FLASK_DEBUG=1 flask run --port 5001

Run everything in one terminal win:
```
python3 manage.py runserver & FLASK_APP=micro_user/main.py flask run --port 5000 & FLASK_APP=micro_data/main.py flask run --port 5001 
```


## Remake the environment

oc delete -f manifests --now && oc create -f manifests && oc get po 

## Start tests
Be in the root of this project and `python3 manage.py test && pytest -v`


## Update app
`kubectl set image deployment/my-deployment <container>=<image>:<new-version>`
`oc set image deploy/data data=VladMasarik/htwg`


oc set image deploy/data data=vladmasarik/htwg-data
oc set image deploy/user user=vladmasarik/htwg-user
oc set image deploy/web web=vladmasarik/htwg-web



oc set image deploy/data data=vladmasarik/htwg-data:latest
oc set image deploy/user user=vladmasarik/htwg-user:latest
oc set image deploy/web web=vladmasarik/htwg-web:latest

## Auto scale


Set limits on the deployments.
Download the metric-server and deploy it.

git clone git@github.com:kubernetes-incubator/metrics-server.git
oc create -f deploy/1.8+/

the create autoscaler

oc autoscale deploy/data --cpu-percent=20 --min=1 --max=10
oc autoscale deploy/user --cpu-percent=20 --min=1 --max=10
oc autoscale deploy/web --cpu-percent=20 --min=1 --max=10


