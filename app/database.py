# Code above omitted 👆

from sqlmodel import SQLModel, create_engine, Session
from fastapi import FastAPI
from .models import Post

postgres_url = "postgresql://postgres:postgres@localhost/fastapi"
engine = create_engine(postgres_url)


def create_db_and_table():
    print("Creating database and table")
    SQLModel.metadata.create_all(engine)

async def lifespan(app: FastAPI):
    create_db_and_table()
    yield


def get_session():
    with Session(engine) as session:
        yield session