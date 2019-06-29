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
kubectl create secret generic aws-web --from-file=./aws-id --from-file=./aws-pass


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
