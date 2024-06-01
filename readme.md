Create an virtualenv and install the requirements:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```


## starting opa server

opa run --server /Users/sachauhan/Documents/GitHub/swisscom-app/opa/policy.rego


## samples
POST
curl -X POST -d '{"name": "John Doe", "email": "john@example.com"}' -H "Authorization: user_tokens" -H "Content-Type: application/json"  http://127.0.0.1:56275/api/users

GET
curl -H "Authorization: user_token" http://localhost:8000/api/users
curl -H "Authorization: admin_token" http://localhost:8000/api/users



docker build -t saijalchauhan/swiss:new .   


 minikube service swiss-service --url



Running opa a docker container with policy

  docker run -v /Users/sachauhan/Documents/GitHub/user-manage/opa/policy.rego:/policy.rego openpolicyagent/opa:edge-rootless run --server policy.rego

  Debug docker container

   curl -X POST -d '{"input": {"role": "admins", "action": "read"}}' http://localhost:8181/v1/data/usermanage/authz

   