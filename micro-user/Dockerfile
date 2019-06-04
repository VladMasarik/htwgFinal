FROM python:3-slim-stretch

WORKDIR /


RUN python3 -m pip install Flask boto3 requests

EXPOSE 5000

COPY ./main.py /
CMD [ "FLASK_APP=main.py flask run" ]