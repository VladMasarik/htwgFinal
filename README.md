# How to

## Build docker files


docker build -t docker.io/vladmasarik/htwg-web .
docker push docker.io/vladmasarik/htwg-web

docker build -t docker.io/vladmasarik/htwg-user ./micro_user
docker push docker.io/vladmasarik/htwg-user

docker build -t docker.io/vladmasarik/htwg-data ./micro_data
docker push docker.io/vladmasarik/htwg-data





oc apply -f manifests



## Create secrets
kubectl create secret generic aws-web \
 --from-file=/home/vmasarik/projects/htwgFinal/aws-id \
 --from-file=/home/vmasarik/projects/htwgFinal/aws-pass \
 --from-file=/home/vmasarik/projects/htwgFinal/gitkey


## Run all servers

Before set the environment variable `HTWGLOCAL` to `true`.
`vi ~/.profile` and write at the end 

```
export HTWGLOCAL=true
export AWS_DEFAULT_REGION=us-west-2
```


python3 manage.py runserver


FLASK_APP=micro_user/main.py FLASK_DEBUG=1 flask run --port 5000


FLASK_APP=micro_data/main.py FLASK_DEBUG=1 flask run --port 5001

Run everything in one terminal win:
```
python3 manage.py runserver & FLASK_APP=micro_user/main.py flask run --port 5000 & FLASK_APP=micro_data/main.py flask run --port 5001 
```


## Remake the environment

oc delete -f manifests --now && oc create -f manifests && oc get po 

## Start tests
Be in the root of this project and `python3 manage.py test && pytest -v`


## Update app
`kubectl set image deployment/my-deployment <container>=<image>:<new-version>`
`oc set image deploy/data data=VladMasarik/htwg`

oc get deployment web -o=jsonpath='{.spec.template.spec.containers[].image}'

oc set image deploy/data data=vladmasarik/htwg-data
oc set image deploy/user user=vladmasarik/htwg-user
oc set image deploy/web web=vladmasarik/htwg-web



oc set image deploy/data data=vladmasarik/htwg-data:latest
oc set image deploy/user user=vladmasarik/htwg-user:latest
oc set image deploy/web web=vladmasarik/htwg-web:latest

## Auto scale


Set limits on the deployments.
Download the metric-server and deploy it.

git clone git@github.com:kubernetes-incubator/metrics-server.git
oc create -f deploy/1.8+/

the create autoscaler

oc autoscale deploy/data --cpu-percent=75 --min=1 --max=3
oc autoscale deploy/user --cpu-percent=75 --min=1 --max=3
oc autoscale deploy/web --cpu-percent=90 --min=1 --max=4


## Scala simulation

```
package computerdatabase

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class RecordedSimulation extends Simulation {

	val httpProtocol = http
		.baseUrl("http://web-default.apps.vmasarik-logging.devcluster.openshift.com")
		.acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
		.acceptEncodingHeader("gzip, deflate")
		.acceptLanguageHeader("en-US,en;q=0.5")
		.upgradeInsecureRequestsHeader("1")
		.userAgentHeader("Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0")



	// scenario("repeat")
	// .repeat(3)( // repeat 3 times
	// 	exec(http("google").get("https://www.example.com"))
	// )

	val scn = scenario("RecordedSimulation")
		.repeat(2)(
		exec(http("request_0")
			.get("/"))
		.pause(10)
		.exec(http("request_1")
			.get("/search?search_term=kubernetes"))
		.pause(8)
		.exec(http("request_2")
			.get("/"))
		.pause(7)
		.exec(http("request_3")
			.get("/profile"))
		.pause(5)
		.exec(http("request_4")
			.get("/"))
		.pause(4)
		.exec(http("request_5")
			.get("/logout/"))
		.pause(2)
		.exec(http("request_6")
			.get("/login/"))
		.pause(5)
		.exec(http("request_7")
			.post("/login/")
			.formParam("csrfmiddlewaretoken", "gpeCyctgZrpigSXKrne4vRXEEu66G9wb4SCqTt5wOcv6quRaDMIKBr82c6JjpYR1")
			.formParam("username", "j")
			.formParam("password", "j")))


	setUp(scn.inject(atOnceUsers(1), rampUsers(50) during (100.seconds))).protocols(httpProtocol)
}
```