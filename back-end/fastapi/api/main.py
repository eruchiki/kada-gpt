from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def hello() -> dict:
    return {"message": "hello World!"}
