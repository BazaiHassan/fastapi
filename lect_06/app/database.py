import json
from typing import Any
from app.schemas import RegisterUserModel


db:dict[Any, Any] = {}

def save(registerInfo:RegisterUserModel):
    db[registerInfo.id] = {**registerInfo.model_dump()}
    with open("db.json", "w") as db_file:
        json.dump(list(db.values()), db_file)