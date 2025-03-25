from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from pydantic import EmailStr


class PostInput(SQLModel):
    title: str
    content: str
    published: Optional[bool] = True

class UserOutput(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

class PostOutput(PostInput):
    id: int
    created_at: datetime
    owner_id: int
    owner : UserOutput

class UserInput(SQLModel):
    email: EmailStr
    password: str

class UserOutput(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    user_id: int
