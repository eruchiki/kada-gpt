from lib.const import *
from datetime import datetime
import ndjson
import os
import tiktoken

LOG_PAHT = "./logs"

# トークン数をカウント
# モデルにはgpt-3.5-turboやtext-embedding-ada-002がある
# なお，gpt-3.5-turboとgpt-4のエンコーディングは同じなので結果は変わらない
def num_tokens_from_string(string, model_name="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def save_chat_log(input_data, retriever_data, select_data_list, compose_data, system_data):
    query, model_type, doc_num = input_data
    token_num = num_tokens_from_string(query)
    input_data_obj = {"query": {"string": query, "token": token_num}, "model_type": model_type, "doc_num": doc_num}

    retriever_data_obj = []
    for num, (relate_doc, doc_score) in enumerate(zip(*retriever_data)):
        retriever_data_obj.append({
            "id": num,
            "document": relate_doc.page_content,
            "filename": relate_doc.metadata["filename"],
            "related_score": doc_score
        })

    total_cost = 0
    select_data_obj = []
    if select_data_list != []:
        for num, select_data in enumerate(select_data_list):
            prompt_str, response, cost, res_format, select_lines = select_data
            select_lines_dst = []
            for select_line_group in select_lines:
                group = []
                for select_line in select_line_group:
                    group.append({"number": select_line.metadata["item_number"], "sentence":select_line.page_content})
                select_lines_dst.append(group)

            total_cost += cost
            prompt_token_num = num_tokens_from_string(prompt_str)
            response_token_num = num_tokens_from_string(response)
            select_data_obj.append({
                "id": num,
                "prompt": {"string": prompt_str, "token": prompt_token_num},
                "response": {"string": response, "token": response_token_num, "formatted_nums": res_format},
                "select_lines": select_lines_dst,
                "cost": cost
            })

    prompt_str, response, cost, res_quote_lines, res_quote_files = compose_data
    total_cost += cost
    prompt_token_num = num_tokens_from_string(prompt_str)
    response_token_num = num_tokens_from_string(response)
    compose_data_obj = {
        "prompt": {"string": prompt_str, "token": prompt_token_num},
        "response": {"string": response, "token": response_token_num},
        "quote": {"quote_lines": res_quote_lines, "quote_files":res_quote_files},
        "cost": cost
    }

    start_time, db_time, select_time, compose_time, method = system_data
    total_time_t = compose_time - start_time
    db_time_t = db_time - start_time
    select_time_t = select_time - db_time
    compose_time_t = compose_time - select_time
    system_data_obj = {
        "start_in": datetime.fromtimestamp(start_time).strftime('%Y/%m/%d %H:%M:%S.%f'),
        "duration": {
            "retriever": db_time_t,
            "select": select_time_t,
            "compose": compose_time_t,
            "total": total_time_t
        },
        "method": method,
        "total_cost": total_cost
    }

    chat_job_obj = {
        "system": system_data_obj,
        "input": input_data_obj,
        "retriever": retriever_data_obj,
        "select": select_data_obj,
        "compose": compose_data_obj
    }

    os.makedirs(LOG_PAHT, exist_ok=True)
    filename = "chat-log.jsonl"
    with open(os.path.join(LOG_PAHT, filename), mode="a", encoding="utf-8") as f:
        writer = ndjson.writer(f, ensure_ascii=False)
        writer.writerow(chat_job_obj)


def save_feedback(message):
    feedback_obj = {
        "chat_date": datetime.fromtimestamp(message["time"]).strftime('%Y/%m/%d %H:%M:%S.%f'),
        "feedback": message["feedback"]
    }

    os.makedirs(LOG_PAHT, exist_ok=True)
    filename = "feedback.jsonl"
    with open(os.path.join(LOG_PAHT, filename), mode="a", encoding="utf-8") as f:
        writer = ndjson.writer(f, ensure_ascii=False)
        writer.writerow(feedback_obj)


def save_emb_log(split_text, total_token):
    emb_log_obj = {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'),
        "split_num": len(split_text),
        "token": [num_tokens_from_string(item) for item in split_text],
        "total_cost": 0.0001 * (total_token / 1000)
    }

    os.makedirs(LOG_PAHT, exist_ok=True)
    filename = "emb-log.jsonl"
    with open(os.path.join(LOG_PAHT, filename), mode="a", encoding="utf-8") as f:
        writer = ndjson.writer(f, ensure_ascii=False)
        writer.writerow(emb_log_obj)
