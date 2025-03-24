from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from pydantic import EmailStr


class PostInput(SQLModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostOutput(PostInput):
    created_at: datetime

class UserInput(SQLModel):
    email: EmailStr
    password: str

class UserOutput(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime
