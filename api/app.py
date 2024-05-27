from flask import Flask, request, jsonify, abort
import requests
import logging
import json
import os


app = Flask(__name__)

# Sample in-memory database
users = [
    {"name": "Saijal Chauhan", "email": "saijalchauhan000@gmail.com"},
    {"name": "Somay Chauhan", "email": "somaychauhan98@gmail.com"}
]

tokens = {"admin_token": "admin", "user_token": "user"}

# Read tokens from environment variables
# tokens = {
#     os.getenv('ADMIN_TOKEN'): 'admin',
#     os.getenv('USER_TOKEN'): 'user'
# }

# Read OPA URL from environment variable
# OPA_URL = os.getenv('OPA_URL')

OPA_URL = "http://localhost:8181/v1/data/usermanage/authz"


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def get_role(token):
    return tokens.get(token)

def is_authorized(role, action):
    try:
        input_data = json.dumps({
            "input": {
                "action": action,
                "role": role
            }
        }, indent=2)
        response = requests.post(OPA_URL, data=input_data)
        app.logger.debug('Authorization check for action "%s" with auth header "%s": %s', action, role, response)
    except Exception as e:
        app.logger.exception("Unexpected error querying OPA.")
        abort(500)
    
    result = response.json().get("result", False)
    is_allowed = result.get("allow", False)
    return is_allowed

@app.route('/api/users', methods=['GET'])
def list_users():
    token = request.headers.get('Authorization')
    app.logger.info('Received request to get users with auth header: %s', token)
    
    role = get_role(token)
    action = 'read'
    if not is_authorized(role,action):
        app.logger.warning('Unauthorized access attempt to get users with auth header: %s', token)
        return jsonify({"error": "User not authorized to read users."}), 403
    
    app.logger.info('User is authorized to list users.')
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    token = request.headers.get('Authorization')
    app.logger.info('Received request to create user with auth header: %s', token)
    
    role = get_role(token)
    action = 'create'
    if not is_authorized(role,action):
        app.logger.warning('Unauthorized access attempt to create user with auth header: %s', role)
        return jsonify({"error": "User not Authorized to create user."}), 403
    
    user = request.json
    if "name" not in user or "email" not in user:
        app.logger.error('Invalid input: %s', user)
        return jsonify({"error": "Invalid Input"}), 400
    
    users.append(user)
    app.logger.info('User authorized to create user, User created: %s', user)
    return jsonify(user), 201



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)