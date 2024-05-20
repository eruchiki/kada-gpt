import requests
import json


collection_data_list = [{"name": "test", "group_id": 1, "create_user_id": 1}]
url = "http://localhost:8000/chat/collections"
for collection_data in collection_data_list:
    response = requests.post(url, data=json.dumps(collection_data))
    print(response)
