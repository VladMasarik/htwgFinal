FROM python:3-slim-stretch

WORKDIR /


RUN python3 -m pip install django==2.2 -U && python3 -m pip install requests
RUN python3 -m pip install Pillow 
RUN apt update && apt install curl -y
EXPOSE 8080
RUN chmod 777 -R /usr/local/lib/python3.7/site-packages/django
COPY ./ /htwgFinal
WORKDIR /htwgFinal


ENTRYPOINT [ "/htwgFinal/init.sh" ]