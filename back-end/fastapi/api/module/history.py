from langchain.memory import ChatMessageHistory


def add_history(chat_history: list) -> ChatMessageHistory:
    history = ChatMessageHistory()
    for human_chat, system_chat in chat_history:
        history.add_user_message(human_chat)
        history.add_ai_message(system_chat)
    return history


# def select_history(query: str, chat_history: list):
