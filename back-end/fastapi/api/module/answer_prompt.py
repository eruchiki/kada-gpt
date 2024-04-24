from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from api.module.template import CHAT_TEMPLATE


# 参考情報の部分
def related_prompt(info_list: list) -> tuple[str, list, list]:
    selected_info_list = [info for info in info_list if info != []]
    selected_info_list = sorted(
        selected_info_list, key=lambda x: x[0][0].metadata["filename"]
    )
    for_log_quote_lines, fileid_list = [], []
    system_template_info = ""
    current_file = ""
    file_num = -1
    item_num = 0
    for info_group in selected_info_list:
        if current_file != info_group[0][0].metadata["filename"]:
            file_num += 1
            item_num = 0
            current_file = info_group[0][0].metadata["filename"]
            fileid_list.append(info_group[0][0].metadata["fileid"])
            system_template_info += f"- [{file_num}] {current_file}\n"
        for info_set in info_group:
            for info in info_set:
                system_template_info += (
                    f"  - [{file_num}-{item_num}] {info.page_content}\n"
                )
                for_log_quote_lines.append(
                    [f"{file_num}-{item_num}", info.page_content]
                )
                item_num += 1
            system_template_info += "\n"
    return system_template_info, fileid_list, for_log_quote_lines


# 質問応答のためのprompt
def create_system_prompt() -> ChatPromptTemplate:
    system_message_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["info"], template=CHAT_TEMPLATE)
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )
    return prompt
