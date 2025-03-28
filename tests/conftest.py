# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
import uuid
from app.main import app
from app.database import get_session
from app.models import User, Post

DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)

# DB override for dependency injection
def override_get_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override
app.dependency_overrides[get_session] = override_get_session

# ---------- Fixtures ----------

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture
def test_user(client):
    email = f"user_{uuid.uuid4().hex[:8]}@test.com"
    password = "testpass"
    payload = {"email": email, "password": password}
    response = client.post("/users", json=payload)
    return {"email": email, "password": password, "id": response.json()["id"]}


@pytest.fixture
def test_user_token(client, test_user):
    response = client.post(
    "/login",
    data={
        "username": test_user["email"],
        "password": test_user["password"]
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.status_code != 200:
        print("Login failed:", response.json())

    token = response.json()["access_token"]
    return token

@pytest.fixture
def auth_headers(test_user_token):
    return {"Authorization": f"Bearer {test_user_token}"}


