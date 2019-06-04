#!/bin/bash

IP=`hostname -I | awk '{print $1}'`

flask run -h $IP -p 8080