import time
from flask import jsonify
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from db.db import (
    save_conversation,
    load_conversations,
    conversations_collection,
    load_conversation,
)
from app.utils import (
    message_to_dict,
    dict_to_message,
)  # Assurez-vous que cet import est correct
from app.template import templates, models

def create_chat(username, chat_name, template, model):
    initial_message = AIMessage(content="Bonjour, comment puis-je vous aider ?")
    new_chat = {
        "chat_name": chat_name,
        "history": [message_to_dict(initial_message)],
        "template": template,
        "model": model,
    }
    save_conversation(username, chat_name, [initial_message], template, model)
    return jsonify({"status": "success", "chat_name": chat_name})


def get_chats(username):
    chats = load_conversations(username)
    for chat in chats:
        chat["history"] = [message_to_dict(msg) for msg in chat["history"]]
    return jsonify({"status": "success", "chats": chats})


def save_message(username, chat_name, message):
    convo = conversations_collection.find_one(
        {"username": username, "chat_name": chat_name}
    )
    if convo:
        convo["chat_history"].append(message_to_dict(HumanMessage(content=message)))
        save_conversation(
            username,
            chat_name,
            [dict_to_message(msg) for msg in convo["chat_history"]],
            convo["template"],
            convo["model"],
        )
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Chat not found"}), 404


def delete_chat(username, chat_name):
    conversations_collection.delete_one({"username": username, "chat_name": chat_name})
    return jsonify({"status": "success"})


def get_response(username, chat_name, user_message):
    convo = conversations_collection.find_one(
        {"username": username, "chat_name": chat_name}
    )
    if not convo:
        return jsonify({"status": "error", "message": "Chat not found"}), 404

    chat_history = [dict_to_message(msg) for msg in convo["chat_history"]]
    template = convo.get("template", "Coder")
    model = convo.get("model", "MIXTRAL 8X7B")

    template_str = templates[template]
    model_str = models[model]

    prompt = ChatPromptTemplate.from_template(template_str)
    llm = ChatGroq(
        temperature=0, model_name=model_str, base_url="https://api.groq.com/"
    )
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"question": user_message, "chat_history": chat_history})
    convo["chat_history"].append(message_to_dict(AIMessage(content=response)))

    save_conversation(
        username,
        chat_name,
        [dict_to_message(msg) for msg in convo["chat_history"]],
        template,
        model,
    )
    return jsonify({"status": "success", "response": response})
