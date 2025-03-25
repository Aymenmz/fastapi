from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from sqlalchemy import Column, Boolean, text, TIMESTAMP
from datetime import datetime

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(nullable=False, index=True)
    
    published: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default=text("true"))
    )

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    )

    owner_id: int = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")

    owner: Optional["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    )
    posts: list[Post] = Relationship(back_populates="owner")
