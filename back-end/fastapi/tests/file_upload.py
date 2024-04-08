import requests

url = "http://localhost:8000/chat/users"
response = requests.get(url)

print(response.json())

url = "http://localhost:8000/chat/collections/1?create_user_id=1"
fileName1 = "./tests/fit.pdf"
fileName2 = "./tests/jasai.pdf"

fileDataBinary1 = open(fileName1, "rb").read()
fileDataBinary2 = open(fileName2, "rb").read()

mime_type = "application/pdf"

fileList = {
    "files": (fileName1, fileDataBinary1, mime_type),
    "files": (fileName2, fileDataBinary2, mime_type),
}

response = requests.post(url, files=fileList)

print(response.json())
