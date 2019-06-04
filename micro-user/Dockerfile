FROM python:3-slim-stretch

WORKDIR /

COPY ./main.py /

RUN python3 -m pip install Flask boto3 requests

EXPOSE 5000

CMD [ "FLASK_APP=main.py flask run" ]