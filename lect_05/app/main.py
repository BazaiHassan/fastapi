from fastapi import FastAPI, HTTPException, status
from typing import Any

from app.schemas import User


db: dict[int, Any] = {
    1: {
        "email": "",
        "first_name": "",
        "last_name": "",
        "age": 0,
        "is_admin": False,
    }
}

app = FastAPI()


@app.post("/user", response_model=User)
def add_user(user: User):
    new_id: int = max(db.keys()) + 1
    db[new_id] = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "type": user.type,
    }
    user = db[new_id]
    return user
