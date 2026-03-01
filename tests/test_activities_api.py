"""
Tests for the Activities API endpoints.
Validates behavior of GET /activities, POST /signup, and DELETE /unregister.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """GET /activities should return all activities with their details."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_contains_required_fields(client):
    """GET /activities should include required fields for each activity."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_signup_for_activity_with_valid_email(client):
    """POST /signup with valid email should add participant to activity."""
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    chess_club = activities_response.json()["Chess Club"]
    assert "newstudent@mergington.edu" in chess_club["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    """POST /signup for non-existent activity should return 404."""
    response = client.post(
        "/activities/Nonexistent%20Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_for_activity_when_already_signed_up_returns_400(client):
    """POST /signup when already signed up should return 400."""
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity_with_valid_participant(client):
    """DELETE /unregister with valid participant should remove them."""
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    chess_club = activities_response.json()["Chess Club"]
    assert "michael@mergington.edu" not in chess_club["participants"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    """DELETE /unregister for non-existent activity should return 404."""
    response = client.delete(
        "/activities/Nonexistent%20Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_when_not_participant_returns_404(client):
    """DELETE /unregister when not a participant should return 404."""
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": "notasignup@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_multiple_signups_and_unregistrations(client):
    """Test sequence of signup and unregister operations."""
    # Sign up for activity
    signup_response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": "alice@mergington.edu"}
    )
    assert signup_response.status_code == 200
    
    # Verify added
    activities_response = client.get("/activities")
    prog_class = activities_response.json()["Programming Class"]
    assert "alice@mergington.edu" in prog_class["participants"]
    original_count = len(prog_class["participants"])
    
    # Unregister
    unregister_response = client.delete(
        "/activities/Programming%20Class/unregister",
        params={"email": "alice@mergington.edu"}
    )
    assert unregister_response.status_code == 200
    
    # Verify removed
    activities_response = client.get("/activities")
    prog_class = activities_response.json()["Programming Class"]
    assert "alice@mergington.edu" not in prog_class["participants"]
    assert len(prog_class["participants"]) == original_count - 1
