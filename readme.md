# User Manage Service

This project is a simple REST API service for managing users. It includes two endpoints:

1. `GET /api/users`: Returns a list of users.
2. `POST /api/users`: Creates a new user.

## Features

- Authenticated users can read the list of users.
- Only users with the "admin" role can create new users.
- Authorization is handled by Open Policy Agent (OPA).
- The service runs in a Kubernetes (k8s) cluster, for example, Minikube.
- Fo

## Prerequisites

- Docker
- Minikube
- Helm
- Python 3.8+
- Open Policy Agent (OPA)

### Simplified Implementation Details

For simplicity, we are using an in-memory database to store users.

Authentication is implemented via dummy tokens.

Example tokens:

- user_token: Represents an authenticated user with a regular role.

- admin_token: Represents an authenticated user with an admin role.

## Setup Instructions

### Step 1: Start Minikube
Start Minikube to create a local Kubernetes cluster. Follow the instructions [here](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Fx86-64%2Fstable%2Fbinary+download) to setup your minikube cluster.
```bash
minikube start
```

### Step 2: Package and install the Helm Chart

Follow the instructions [here](https://helm.sh/docs/intro/install/) to install helm localy.

```bash
helm package chart/

helm install <release-name> <chart>.tgz  -n <namespace>
```

#### OR Setup Helm Repo and install Chart
 
```bash
helm repo add swisscom-helm https://saijal.jfrog.io/artifactory/api/helm/swisscom-helm --username <username> --password <password>
```

```bash
helm install <release-name> swisscom-helm/user_manage --version 0.1.0 -n <namespace>
```

### Step 3: Port forward the service using minkube command

```bash
minikube service <usermanage-service-name> --url -n <namespace>
```

### Step 4: Testing API endpoints

Use these commands to test API functionality

```bash
curl -H "Authorization: user_token" http://<minikube-endpoint>/api/users
```
