from fastapi import FastAPI
from app.schemas import  RegisterUserModel
from app.database import save

app = FastAPI()

@app.post("/user/register", response_model=RegisterUserModel)
def register_user(registerInfo:RegisterUserModel):
    
    save(registerInfo=registerInfo)
    return {
        "data": "saved"
    }

@app.post("/user/login")
def login_user():
    return

@app.get("/users")
def get_all_users():
    return
@app.get("/user/{id}")
def get_user_profile(id:str):
    return