#!/bin/bash
IP=`hostname -I | awk '{print $1}'`
sudo python3 manage.py runserver $IP:80