"""
Shared test fixtures for the Mergington High School Activities API.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provides a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to seed state before and after each test.
    This ensures tests are isolated and do not interfere with each other.
    """
    # Original seed state
    seed_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team-based soccer training and inter-school matches",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Develop basketball skills through drills and friendly games",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu", "elijah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Practice acting, stage performance, and school productions",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["mia@mergington.edu", "james@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed-media art projects",
            "schedule": "Fridays, 2:30 PM - 4:00 PM",
            "max_participants": 15,
            "participants": ["charlotte@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Build public speaking and critical thinking through debates",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["amelia@mergington.edu", "henry@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science challenges and collaborative experiments",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "benjamin@mergington.edu"]
        }
    }

    # Reset before test
    activities.clear()
    activities.update(seed_state)

    yield

    # Reset after test
    activities.clear()
    activities.update(seed_state)
