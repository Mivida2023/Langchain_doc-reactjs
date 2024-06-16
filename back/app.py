from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import create_chat, get_chats, save_message, delete_chat, get_response
from db import init_db, delete_conversation, get_models, get_templates
from config import DEFAULT_USER
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


def validate_environment_variables():
    required_vars = [
        "MONGODB_URI",
        "MONGODB_DB_NAME",
        "GROQ_MODEL_LLAMA3_8B",
        "GROQ_MODEL_LLAMA3_70B",
        "GROQ_MODEL_MIXTRAL_8X7B",
        "GROQ_MODEL_GEMMA_7B_IT",
        "DEFAULT_USER",
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"The environment variable {var} is not set or invalid.")


# Validate environment variables before initializing the database
validate_environment_variables()

# Initialize MongoDB
init_db()


@app.route("/models", methods=["GET"])
def models_route():
    return jsonify(get_models())


@app.route("/templates", methods=["GET"])
def templates_route():
    return jsonify(get_templates())


@app.route("/chats/<username>", methods=["POST"])
def create_chat_route(username):
    data = request.json
    return create_chat(username, data["chat_name"], data["template"], data["model"])


@app.route("/chats/<username>", methods=["GET"])
def get_chats_route(username):
    return get_chats(username)


@app.route("/chats/message/<username>", methods=["POST"])
def save_message_route(username):
    try:
        data = request.json
        print("Received payload for save_message_route: ", data)
        return save_message(username, data["chat_name"], data["message"])
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/chats/delete/<username>", methods=["POST"])
def delete_chat_route(username):
    try:
        data = request.json
        print("Received payload for delete_chat_route: ", data)
        delete_conversation(
            username, data["chat_name"]
        )  # Utilisez delete_conversation ici
        return jsonify({"status": "success"})
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/chats/response/<username>", methods=["POST"])
def get_response_route(username):
    try:
        data = request.json
        print("Received payload for get_response_route: ", data)
        return get_response(username, data["chat_name"], data["message"])
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
