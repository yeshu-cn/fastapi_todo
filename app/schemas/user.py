from typing import List
from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role: UserRole

class UserUpdate(UserBase):
    role: UserRole

class UserInDB(UserBase):
    id: int
    role: UserRole

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class TokenRefresh(BaseModel):
    refresh_token: str

class UserLogin(BaseModel):
    username: str
    password: str