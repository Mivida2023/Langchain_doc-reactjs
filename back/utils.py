from langchain_core.messages import AIMessage, HumanMessage


def message_to_dict(message):
    """
    Convert a LangChain message object to a dictionary.

    Args:
    message (Union[AIMessage, HumanMessage]): The message object to convert.

    Returns:
    dict: A dictionary representation of the message.
    """
    if isinstance(message, AIMessage):
        return {"type": "AI", "content": message.content}
    elif isinstance(message, HumanMessage):
        return {"type": "Human", "content": message.content}
    else:
        raise ValueError("Unknown message type")


def dict_to_message(message_dict):
    """
    Convert a dictionary to a LangChain message object.

    Args:
    message_dict (dict): The dictionary to convert.

    Returns:
    Union[AIMessage, HumanMessage]: The message object.
    """
    if message_dict["type"] == "AI":
        return AIMessage(content=message_dict["content"])
    elif message_dict["type"] == "Human":
        return HumanMessage(content=message_dict["content"])
    else:
        raise ValueError("Unknown message type")

