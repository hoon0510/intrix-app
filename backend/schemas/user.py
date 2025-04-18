from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    credit: float

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True 