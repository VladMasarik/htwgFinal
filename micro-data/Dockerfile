FROM python:3-slim-stretch

WORKDIR /


RUN python3 -m pip install Flask boto3 requests

EXPOSE 5000

COPY ./init.sh /


COPY ./main.py /

RUN chmod a+x /init.sh

ENV FLASK_APP=main.py
ENTRYPOINT [ "/init.sh" ]