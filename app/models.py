from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(nullable=False, index=True)
    
    published: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner_id: int = Field(foreign_key="users.id")

    owner: Optional["User"] = Relationship(back_populates="posts")


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    posts: List[Post] = Relationship(back_populates="owner")


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
   
    post_id: int = Field(foreign_key="posts.id", primary_key=True)
    user_id: int = Field(foreign_key="users.id", primary_key=True)
