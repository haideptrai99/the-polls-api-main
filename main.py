from fastapi import FastAPI

from app.models.Polls import PollCreate

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/polls/create")
def create_poll(poll: PollCreate):
    new_poll = poll.create_poll()
    return {"detail": "Poll sucesss created", "poll_id": new_poll.id, "poll": new_poll}


# choice_data = Choice(description="hehe", label=1)

# Objective:
# -- split the Poll model into
# 1. PollCreate: the write model:
#     * title (required)
#     * options (list of strings)
#     * expires_at (optional datetime)
#
# 2. Poll: the read model
#     * id (uuid with default factory)
#     * options (list of Choice)
#     * created_at (optional datetime)
