FROM python:3-slim-stretch

WORKDIR /


RUN python3 -m pip install django==2.2 -U && python3 -m pip install requests
RUN python3 -m pip install Pillow 

EXPOSE 8080
COPY ./ /htwgFinal
WORKDIR /htwgFinal

ENTRYPOINT [ "/htwgFinal/init.sh" ]