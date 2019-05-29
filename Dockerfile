FROM python:3-slim-stretch

WORKDIR /

COPY htwgFinal /
WORKDIR /htwgFinal

EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "127.0.0.1:8080"]