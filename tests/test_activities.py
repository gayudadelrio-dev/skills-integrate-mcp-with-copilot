import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app import app

client = TestClient(app)


def test_github_skills_activity_exists_and_is_signupable():
    response = client.get("/activities")
    assert response.status_code == 200

    activities = response.json()
    assert "GitHub Skills" in activities
    assert activities["GitHub Skills"]["description"] == (
        "Learn practical coding and collaboration skills with GitHub"
    )

    signup_response = client.post(
        "/activities/GitHub%20Skills/signup?email=student@mergington.edu"
    )
    assert signup_response.status_code == 200

    refreshed = client.get("/activities")
    assert "student@mergington.edu" in refreshed.json()["GitHub Skills"]["participants"]
