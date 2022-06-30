# Build and Deploy Flask app with full CI/CD # 
In this project we will use:
1.  Google cloud K8s cluster (some with helm)
2.  Github
3.  Docker & docker-compose
4.  Flask app
5.  Terraform
6.  Mongodb
7.  Nginx ingress controller (with TLS)
8.  EFK
9.  Grafana & Prometheus
10. Jenkins
11. ArgoCD

### Working Tree:


## To build the app localy:
Install docker and docker-compose first

    docker-compose up --build

That command will create 3 containers locally

### === DNS URI === 
Enter the website to create your own dns uri for use in this project:

https://www.noip.com/


https://meirapp.ddns.net/

### === Github repo === #
Upload your app code to github for future use

git@github.com:shay1987/feedbackapp.git

## 1. building the cluster in GCP: ##
Before you start using the gcloud CLI and Terraform, you have to install the Google Cloud SDK bundle.

You can find the official documentation on installing Google Cloud SDK here:
https://cloud.google.com/sdk/docs/install

Next, you need to link your account to the gcloud CLI, and you can do this with:

    gcloud init
    gcloud auth application-default login
    gcloud services enable storage.googleapis.com

### Creating buckt (for tfstat file)
    gsutil mb -p feisty-deck-351210 gs://feedback-pro

First step is to provision a cluster using Terraform files located in terraform folder:

variables.tf - to define the parameters for the cluster.  (make sure to copy project id from gcp)

main.tf - to store the actual code for the cluster.

outputs.tf - to define the outputs.

provider.tf - define the cloud provider

Next use these commands to apply the files:

    terraform init
    terraform plan
    terraform apply

Note - it will take a few minutes to deploy

what happend?
Terraform created cluster in Gcloud and bucket to save the state-file that was created.

## 2. Connecting to the cluster:
    gcloud container clusters get-credentials feedback-prod --region europe-west1 --project feisty-deck-351210

Enable the Cloud Storage API:

    gcloud services enable storage.googleapis.com

## 3. creating Namespace:
    kubectl create namespace feedback

## 4. mongodb build
In the main folder:

    helm repo add bitnami https://charts.bitnami.com/bitnami
    
    ??? helm install mongo -n feedback -f mongo.yaml bitnami/mongodb
    helm install mongo -n feedback -f mongo.yaml bitnami/mongodb --version 10.15.0

## 5. ingress install:
In the ingress folder use these commands:

    helm repo add jetstack https://charts.jetstack.io
    helm install cert-manager --namespace feedback jetstack/cert-manager
    # May print FAILURE but install was secsseful, look at gcp #
    kubectl apply -f letsencrypt-prod.yaml

    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.0/deploy/static/provider/cloud/deploy.yaml

    kubectl apply -f ingress.yaml

## 6. create and install feedback app:
get inside the app folder

    docker build -t feed .

that will build an image of the app
next push it to your cloud repo for using it at gcp you will have to use these commands:
    
    docker tag feed gcr.io/project_name/feed
    docker tag feed gcr.io/astral-archive-351007/feed
    docker push gcr.io/project_name/feed
    docker push gcr.io/astral-archive-351007/feed

If you got an error during the push because of the authentication enter :
    https://cloud.google.com/container-registry/docs/advanced-authentication

in the feedback main folder run the command:

    kubectl apply -f deployment.yaml

## 2. Jenkins install 
At first run inside jenkins folder the command:

    docker build -t jenkins .
    
that will build an image of jenkins
next push it to your cloud repo for using it while installing jenkins, at gcp you will have to use these commands:

    docker tag jenkins gcr.io/project_name/jenkins
    docker push gcr.io/project_name/jenkins

make sure to cahnge the image path in the values.yaml file (line 21) then run these commands:

    helm repo add jenkinsci https://charts.jenkins.io
    helm repo update

we will build a PV for jenkins:
    kubectl apply -f jenkinsvol.yaml

we will build jenkins with role:
    kubectl apply -f jenkinsa.yaml

    helm install jenkins -f values.yaml jenkinsci/jenkins

To enter jenkins UI:

    export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/component=jenkins-master" -l "app.kubernetes.io/instance=cd-jenkins" -o jsonpath="{.items[0].metadata.name}")
    
    kubectl port-forward $POD_NAME 8080:8080 >> /dev/null 2>&1 &


## 5. building ARGOCD
### ArgoCD tutorial
https://argo-cd.readthedocs.io/en/stable/getting_started/


    kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/core-install.yaml

### Get Password
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

    Username: admin

### ArgoCD UI
    kubectl port-forward svc/argocd-repo-server 8080:443

# === SSH tutorial === #
https://www.youtube.com/watch?v=8X4u9sca3Io 

# === TLS tutorial === #
https://docs.bitnami.com/tutorials/secure-kubernetes-services-with-ingress-tls-letsencrypt

    helm repo add jetstack https://charts.jetstack.io
    kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.14.1/cert-manager.crds.yaml
    helm install cert-manager -n feedback jetstack/cert-manager --version v0.14.1



# Logging with EFK in Kubernetes
Get inside the EFK folder and use these commands to install EFK:

    helm repo add elastic https://helm.elastic.co
    helm install elasticsearch -n feedback -f elastic.yaml --version 7.17.3 elastic/elasticsearch
wait for few minutes..

    helm repo add fluent https://fluent.github.io/helm-charts
    helm upgrade -i fluent-bit -n feedback fluent/fluent-bit -f fluentd-daemonset-elasticsearch.yaml
    helm install kibana -n feedback elastic/kibana -f kibana-values.yaml

Open Kibana dashboard via loadbalncer ip

# Building Prom + grafana

Get inside the prom folder and follow these commands:

    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

    helm install prometheus -n feedback prometheus-community/kube-prometheus-stack --values values.yaml

to enter prometheus:
kubectl port-forward -n feedback service/prometheus-kube-prometheus-prometheus 9090:9090
then enter localhost:9090

install grafana:

    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update
    helm upgrade --install promtail -n feedback grafana/promtail -f promtail-values.yaml
    helm upgrade --install loki -n feedback grafana/loki-distributed

to enter grafana:
kubectl port-forward -n feedback service/prometheus-grafana 3000:80
enter localhost:3000

וusername: admin
Password: prom-operator

