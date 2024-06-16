from flask import Blueprint, request, jsonify
from app.chat import create_chat, get_chats, save_message, get_response
from db.db import delete_conversation  # Assurez-vous que cet import est correct

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/<username>", methods=["POST"])
def create_chat_route(username):
    data = request.json
    return create_chat(username, data["chat_name"], data["template"], data["model"])


@chat_bp.route("/<username>", methods=["GET"])
def get_chats_route(username):
    return get_chats(username)


@chat_bp.route("/message/<username>", methods=["POST"])
def save_message_route(username):
    try:
        data = request.json
        print("Received payload for save_message_route: ", data)
        return save_message(username, data["chat_name"], data["message"])
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400


@chat_bp.route("/delete/<username>", methods=["POST"])
def delete_chat_route(username):
    try:
        data = request.json
        print("Received payload for delete_chat_route: ", data)
        delete_conversation(username, data["chat_name"])
        return jsonify({"status": "success"})
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400


@chat_bp.route("/response/<username>", methods=["POST"])
def get_response_route(username):
    try:
        data = request.json
        print("Received payload for get_response_route: ", data)
        return get_response(username, data["chat_name"], data["message"])
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400
