import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = "pytestuser@mergington.edu"
    activity = "Basketball Team"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Check participant is present
    activities = client.get("/activities").json()
    assert test_email in activities[activity]["participants"]

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 200
    assert f"Removed {test_email}" in response.json()["message"]

    # Check participant is removed
    activities = client.get("/activities").json()
    assert test_email not in activities[activity]["participants"]
