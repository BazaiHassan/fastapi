from fastapi import FastAPI, HTTPException, status
from typing import Any

app = FastAPI()

s_database = {1: {"first name": "Ali", "last name":"Hosseini", "age":34}, 2: {"first name": "Hami", "last name":"Leyla", "age":23}}


@app.get("/all")
def get_all():
    return {
        "data":s_database
    }

@app.put("/profile")
def update_profile(id: int, firstName: str, age:int, lastName:str) -> dict[str, Any]:
    s_database[id] = {"first name": firstName, "last name":lastName, "age":age}
    return {
        "data":s_database
    }


@app.patch("/profile")
def update_profile_key(id: int, body:dict[str, Any]):
    person = s_database[id]

    person.update(body)

    s_database[id] = person

    return {
        "data":s_database
    } 

@app.delete("/delete")
def delete_person(id:int):
    s_database.pop(id)
    return {
        "message":f"The ID {id} is deleted",
        "data":s_database
    }
