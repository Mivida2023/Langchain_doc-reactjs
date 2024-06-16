from flask import jsonify

valid_users = {
    "user1": "password1",
    "user2": "password2",
}


def login(username, password):
    if valid_users.get(username) == password:
        return jsonify({"status": "success", "username": username})
    else:
        return (
            jsonify({"status": "error", "message": "Invalid username or password"}),
            401,
        )
