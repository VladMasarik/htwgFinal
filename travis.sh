#!/bin/bash
set -ev
python3 manage.py runserver &
FLASK_APP=micro_user/main.py flask run --port 5000 &
FLASK_APP=micro_data/main.py flask run --port 5001 &
python3 manage.py test
pytest -v

docker login -u vladmasarik -p $DOCKERPASS

docker build -t docker.io/vladmasarik/htwg-web .
docker push docker.io/vladmasarik/htwg-web

docker build -t docker.io/vladmasarik/htwg-user ./micro_user
docker push docker.io/vladmasarik/htwg-user

docker build -t docker.io/vladmasarik/htwg-data ./micro_data
docker push docker.io/vladmasarik/htwg-data