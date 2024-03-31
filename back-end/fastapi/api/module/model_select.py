from typing import Any
from langchain.chat_models import ChatOpenAI


def select_model(model_name: str) -> Any:
    llm = ChatOpenAI(temperature=0, model=model_name, timeout=300)
    return llm
