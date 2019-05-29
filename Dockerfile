FROM python:3-slim-stretch

WORKDIR /

COPY ./ /htwgFinal
WORKDIR /htwgFinal

RUN python3 -m pip install django==2.2 -U && python3 -m pip install requests
RUN python3 -m pip install Pillow 

EXPOSE 8080

ENTRYPOINT [ "/htwgFinal/init.sh" ]