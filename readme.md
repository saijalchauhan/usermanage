Create an virtualenv and install the requirements:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```


## starting opa server

opa run --server /Users/sachauhan/Documents/GitHub/swisscom-app/opa/policy.rego


## samples
curl -H "Authorization: admin_token" -X POST -d '{"name": "John Doe", "email": "john@example.com"}' -H "Content-Type: application/json" http://localhost:8000/api/users 


curl -H "Authorization: user_token" http://localhost:8000/api/users

curl -H "Authorization: admin_token" http://localhost:8000/api/users



 docker build -t swiss:new .   