# Code above omitted 👆

from sqlmodel import create_engine, Session
from .config import settings


postgres_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(postgres_url)


# def create_db_and_table():
#     print("Postgres URL:", postgres_url)
#     print("Creating database and table")
#     SQLModel.metadata.create_all(engine)

# async def lifespan(app: FastAPI):
#     create_db_and_table()
#     yield


def get_session():
    with Session(engine) as session:
        yield session