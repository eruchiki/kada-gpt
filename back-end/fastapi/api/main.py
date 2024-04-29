from fastapi import FastAPI
from api.routers import users, threads, collections, groups
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app = FastAPI()
app.include_router(users.router)
app.include_router(threads.router)
app.include_router(collections.router)
app.include_router(groups.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # 認証情報のアクセスを許可(今回は必要ない)
    allow_credentials=True,
    # 全てのリクエストメソッドを許可(["GET", "POST"]など個別指定も可能)
    allow_methods=["*"],
    allow_headers=["*"],
)
