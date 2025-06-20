from pydantic import BaseModel, Field
from enum import Enum

class UserType(Enum):
    admin = "admin"
    user = "user"
    author = "author"

class User(BaseModel):
    email: str = Field(description="This field must be filled with a correct email",max_length=255)
    first_name: str
    last_name: str
    age: int = Field(gt=18)
    type: UserType = UserType.user