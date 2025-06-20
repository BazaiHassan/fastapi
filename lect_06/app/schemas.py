from pydantic import BaseModel, Field
from typing import Any
import uuid

class BaseUser(BaseModel):
    id: Any = Field(default=uuid.uuid4())
    email: str
    password: str

class RegisterUserModel(BaseUser):
    confirm_password:str
    name: str
    age: int
    city: str
    isStudent: bool


class LoginUserModel(BaseUser):
    pass
