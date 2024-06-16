from flask import Blueprint, jsonify
from db.db import get_models, get_templates

model_bp = Blueprint("model", __name__)


@model_bp.route("/models", methods=["GET"])
def models_route():
    try:
        models = get_models()
        return jsonify({"status": "success", "models": models})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@model_bp.route("/templates", methods=["GET"])
def templates_route():
    try:
        templates = get_templates()
        return jsonify({"status": "success", "templates": templates})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
