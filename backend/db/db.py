import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv
from app.utils import message_to_dict, dict_to_message

load_dotenv()

# Initialize MongoDB client with SSL support
client = MongoClient(os.getenv("MONGODB_URI"), ssl=True)
db = client[os.getenv("MONGODB_DB_NAME")]

# Define collections
conversations_collection = db["conversations"]
users_collection = db["users"]


def init_db():
    if not os.getenv("MONGODB_URI"):
        raise ValueError("The environment variable MONGODB_URI is not set.")
    if not os.getenv("MONGODB_DB_NAME"):
        raise ValueError("The environment variable MONGODB_DB_NAME is not set.")
    if "conversations" not in db.list_collection_names():
        db.create_collection("conversations")
    if "users" not in db.list_collection_names():
        db.create_collection("users")
    if "models" not in db.list_collection_names():
        db.create_collection("models")
        db.models.insert_many(
            [
                {"name": os.getenv("GROQ_MODEL_LLAMA3_8B")},
                {"name": os.getenv("GROQ_MODEL_LLAMA3_70B")},
                {"name": os.getenv("GROQ_MODEL_MIXTRAL_8X7B")},
                {"name": os.getenv("GROQ_MODEL_GEMMA_7B_IT")},
            ]
        )
    if "templates" not in db.list_collection_names():
        db.create_collection("templates")
        db.templates.insert_many([{"name": "Coder"}, {"name": "Monty"}])


def save_conversation(username, chat_name, chat_history, template=None, model=None):
    chat_history_dicts = [message_to_dict(message) for message in chat_history]
    update_data = {"chat_history": chat_history_dicts, "last_used": time.time()}
    if template:
        update_data["template"] = template
    if model:
        update_data["model"] = model
    conversations_collection.update_one(
        {"username": username, "chat_name": chat_name},
        {"$set": update_data},
        upsert=True,
    )


def load_conversations(username):
    user_conversations = conversations_collection.find({"username": username}).sort(
        "last_used", -1
    )
    conversations = []
    for convo in user_conversations:
        conversations.append(
            {
                "name": convo["chat_name"],
                "history": [dict_to_message(msg) for msg in convo["chat_history"]],
                "last_used": convo["last_used"],
                "template": convo["template"],
                "model": convo["model"],
            }
        )
    return conversations


def load_conversation(username, chat_name):
    convo = conversations_collection.find_one(
        {"username": username, "chat_name": chat_name}
    )
    if convo:
        chat_history = [dict_to_message(msg) for msg in convo["chat_history"]]
        return {
            "name": convo["chat_name"],
            "history": chat_history,
            "last_used": convo["last_used"],
            "template": convo["template"],
            "model": convo["model"],
        }
    return None


def delete_conversation(username, chat_name):
    conversations_collection.delete_one({"username": username, "chat_name": chat_name})


def get_models():
    return [model["name"] for model in db.models.find()]


def get_templates():
    return [template["name"] for template in db.templates.find()]
