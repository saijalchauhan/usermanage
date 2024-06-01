from flask import Flask, request, jsonify, abort
import requests
import logging
import json
import os


app = Flask(__name__)

# Sample in-memory database
users = [
    {"name": "Saijal Chauhan", "email": "saijalchauhan000@gmail.com"},
    {"name": "Somay Chauhan", "email": "somaychauhan98@gmail.com"},
]

# Dummy token to user mapping from environment variable
tokens = {
    "admin_token": os.getenv("ADMIN_TOKEN"),
    "user_token": os.getenv("USER_TOKEN"),
}

# Read OPA URL from environment variable
OPA_URL = os.getenv("OPA_URL")


# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s"
)


def get_role(token):
    return tokens.get(token)


def is_authorized(role, action):
    try:
        input_data = json.dumps({"input": {"action": action, "role": role}}, indent=2)
        response = requests.post(OPA_URL, data=input_data)
        app.logger.debug('Authorization check for action "%s" : %s', action, response)
    except Exception as e:
        app.logger.exception("Unexpected error querying OPA.")
        abort(500)

    result = response.json().get("result", False)
    is_allowed = result.get("allow", False)
    app.logger.debug('`Is authorized by OPA`: "%s"', is_allowed)
    return is_allowed


@app.route("/api/users", methods=["GET"])
def list_users():
    token = request.headers.get("Authorization")
    app.logger.info("Received request to get users with auth header: %s", token)

    role = get_role(token)
    action = "read"
    if not is_authorized(role, action):
        app.logger.warning(
            "Unauthorized access attempt to get users with auth header: %s", token
        )
        return jsonify({"error": "User not authorized to read users."}), 403

    app.logger.info("User is authorized to list users.")
    return jsonify(users)


@app.route("/api/users", methods=["POST"])
def create_user():
    token = request.headers.get("Authorization")
    app.logger.info("Received request to create user with auth header: %s", token)

    role = get_role(token)
    action = "create"
    if not is_authorized(role, action):
        app.logger.warning(
            "Unauthorized access attempt to create user with auth header: %s", role
        )
        return jsonify({"error": "User not Authorized to create user."}), 403

    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return (
            jsonify({"error": "Invalid input. 'name' and 'email' are required."}),
            400,
        )

    # Check for extra parameters
    allowed_keys = {"name", "email"}
    if any(key not in allowed_keys for key in data):
        return (
            jsonify({"error": "Invalid input. Only 'name' and 'email' are allowed."}),
            400,
        )

    new_user = {"name": data["name"], "email": data["email"]}

    users.append(new_user)
    app.logger.info("User is authorized to create user, User created: %s", new_user)
    return jsonify(new_user), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
