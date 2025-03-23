from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class PostInput(SQLModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostOutput(PostInput):
    created_at: datetime