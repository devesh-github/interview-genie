
import os
import tempfile

# Use a separate database for tests.
_test_dir = tempfile.TemporaryDirectory()
os.environ["INTERVIEW_GENIE_TEST_DIR"] = _test_dir.name

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSession = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

Base.metadata.create_all(bind=engine)


def override_db():
    with TestingSession() as db:
        yield db


app.dependency_overrides[get_db] = override_db

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_profile_and_skills():
    profile = {
        "name": "Test User",
        "role": "Software Engineer",
        "experience_years": 5,
        "target_company": "Google",
    }

    response = client.put("/api/profile", json=profile)
    assert response.status_code == 200
    assert response.json()["role"] == "Software Engineer"

    response = client.get("/api/profile")
    assert response.status_code == 200

    skill = {
        "name": "Python",
        "level": "Advanced",
        "priority": "High",
    }

    response = client.post("/api/skills", json=skill)
    assert response.status_code == 201

    skill_id = response.json()["id"]

    response = client.get("/api/skills")
    assert len(response.json()) == 1

    response = client.delete(f"/api/skills/{skill_id}")
    assert response.status_code == 204

    response = client.get("/api/skills")
    assert response.json() == []
