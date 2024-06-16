from flask import Blueprint, request, jsonify
from app.auth import authenticate, register

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if authenticate(username, password):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@auth_bp.route("/register", methods=["POST"])
def register_route():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return register(username, password)
