# coding: utf-8
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    friends: list


@app.get("/")
def index():
    return {"admin": "welcome to FastAPI"}


@app.get("/users/{user_id}")
def read_user(user_id: int, name: str = None):
    return {"user_id": user_id, "name": name}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {"user_name": user.name, "user_id": user_id}
