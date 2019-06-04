# How to

## Build docker files
docker build -t docker.io/vladmasarik/htwg-web .
docker push docker.io/vladmasarik/htwg-web

docker build -t docker.io/vladmasarik/htwg-user ./micro-user
docker push docker.io/vladmasarik/htwg-user

docker build -t docker.io/vladmasarik/htwg-data ./micro-data
docker push docker.io/vladmasarik/htwg-data

## Create secrets
kubectl create secret generic aws-web --from-file=./aws-id --from-file=./aws-pass