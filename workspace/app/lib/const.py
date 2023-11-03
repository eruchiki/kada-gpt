class ConstMeta(type):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f'Can\'t rebind const ({name})')
        else:
            self.__setattr__(name, value)

class StSession(metaclass=ConstMeta):
    MODEL_RADIO = "model_radio"
    MODEL_RADIO_TMP = "model_radio_tmp"
    MODEL_NAME = "model_name"
    MODEL_OPTIONS = {"GPT-3.5": "gpt-3.5-turbo",
                    "GPT-3.5-16k": "gpt-3.5-turbo-16k",
                    "GPT-4": "gpt-4",
                    "GPT-4-32k": "gpt-4-32k"}
    MAX_TOKEN = "max_token"
    CHAT_QUERY = "chat_query"
    CHAT_QUERY_TMP = "chat_query_tmp"
    CHAT_ANSWER = "chat_answer"
    CHAT_RELATE = "chat_relate"
    CHAT_REFERENCE_NUMS = "chat_reference_nums"
    CHAT_REFERENCE_NUMS_TMP = "chat_reference_nums_tmp"
    CHAT_INPUT_TOKEN = "chat_input_token"
    CHAT_MESSAGES = "chat_messages"