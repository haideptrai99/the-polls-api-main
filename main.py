from fastapi import FastAPI

from app.models.Polls import Poll

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/polls/create")
def create_poll():
    return Poll(options=["yes", "no", "maybe"])
