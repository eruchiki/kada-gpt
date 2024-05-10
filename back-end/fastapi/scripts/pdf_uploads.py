from glob import glob
import requests


# 自分のuserIdに変更
USER_ID = 0
# 格納したいcollection idに変更
COLLECTION_ID = 0


url = f"http://localhost:8000/chat/collections/{COLLECTION_ID}?create_user_id={USER_ID}"
mime_type = "application/pdf"
uploads_list = []
for file in glob("./pdf/*.pdf"):
    fileDataBinary = open(file, "rb").read()
    uploads_list.append(("files", (file, fileDataBinary, mime_type)))
response = requests.post(url, files=uploads_list)
