#!/bin/bash
string=$(oc get deployment web -o=jsonpath='{.spec.template.spec.containers[].image}')
if [[ $string == *":latest"* ]]; then
    oc set image deploy/data data=vladmasarik/htwg-data
    oc set image deploy/user user=vladmasarik/htwg-user
    oc set image deploy/web web=vladmasarik/htwg-web
else
    oc set image deploy/data data=vladmasarik/htwg-data:latest
    oc set image deploy/user user=vladmasarik/htwg-user:latest
    oc set image deploy/web web=vladmasarik/htwg-web:latest

fi



