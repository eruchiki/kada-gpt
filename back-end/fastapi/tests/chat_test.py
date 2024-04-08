import requests


def user_test() -> tuple[int, int]:
    group_data = {"name": "test_group"}
    res = requests.post(
        "http://localhost:8080/chat/groups", json=group_data
    )
    print(res.json())
    group_id = res.json()["id"]
    user_data = {"name": "test_user",
                 "email": "hogehoge@gmail.com",
                 "password": "password",
                 "group_id" : group_id}
    res = requests.post(
        "http://localhost:8080/chat/groups", json=user_data
    )
    print(res.json())
    user_id = res.json()["id"]
    return group_id, user_id


def collection_test(user_id: int) -> int:
    collection_data = {"name": "test_collection",
                       "create_user_id": user_id}
    res = requests.post(
        "http://localhost:8080/chat/groups", json=collection_data
    )
    print(res.json())
    collection_id: int = res.json()["id"]
    return collection_id


def thread_test(user_id: int, group_id: int, collecitno_id: int) -> None:
    thread_data = {"name": "test_thread",
                   "model_name": "gpt4",
                   "relate_num": 4,
                   "group_id": group_id}

# def document_test():


# def chat_test(user_id,thread_id):
