from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from db.db import users_collection


def authenticate(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        return True
    return False


def register(username, password):
    if users_collection.find_one({"username": username}):
        return jsonify({"status": "error", "message": "User already exists"}), 400
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({"username": username, "password": hashed_password})
    return jsonify({"status": "success"}), 200
