import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Signup
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg.status_code == 200
    # Unregister again should fail
    response_unreg2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg2.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 308)  # Redirect or OK
