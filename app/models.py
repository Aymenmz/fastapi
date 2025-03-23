from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import Column, Boolean, text, TIMESTAMP
from datetime import datetime

class Post(SQLModel, table=True):
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
