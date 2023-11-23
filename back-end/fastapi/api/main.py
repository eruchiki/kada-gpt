from fastapi import FastAPI
from api.routers import users, threads, collections


app = FastAPI()
app.include_router(users.router)
app.include_router(threads.router)
app.include_router(collections.router)
