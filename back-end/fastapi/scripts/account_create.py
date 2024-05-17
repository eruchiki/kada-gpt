import requests
import json

group_url = "http://localhost:8000/chat/groups"

group_name_list = ["test2"]
for group_name in group_name_list:
    response = requests.post(group_url, data=json.dumps({"name": group_name}))
    print(response)

user_data_list = [
    {
        "name": "ganbon",
        "email": "hogehoge2@gmail.com",
        "password": "fugafuga2",
        "group_id": 1,
    }
]
user_url = "http://localhost:8000/chat/users"
for user in user_data_list:
    response = requests.post(user_url, data=json.dumps(user))
    print(response)
