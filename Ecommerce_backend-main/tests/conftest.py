import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from models import cart, orders, order_items, user, product, category

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    from core.cache import redis_client
    redis_client.flushdb()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def admin_token(client):
    client.post("/auth/register", json={
        "username": "adminuser",
        "email": "admin@test.com",
        "password": "test1234"
    })

    from models.user import User, UserRole
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "adminuser").first()
    user.role = UserRole.admin
    db.commit()
    db.close()

    login_response = client.post("/auth/login", data={
        "username": "adminuser",
        "password": "test1234"
    })
    return login_response.json()["access_token"]
