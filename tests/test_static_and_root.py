"""
Tests for static files and root redirect behavior.
Validates the / root endpoint and /static file accessibility.
"""

import pytest


def test_root_redirects_to_static_index(client):
    """GET / should redirect to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_root_with_follow_redirects(client):
    """GET / with follow_redirects should serve index.html."""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    # Response should contain HTML content from index.html
    content = response.text
    assert "<!DOCTYPE html>" in content or "<html" in content


def test_static_index_html_accessible(client):
    """GET /static/index.html should be accessible."""
    response = client.get("/static/index.html")
    assert response.status_code == 200
    content = response.text
    assert "<!DOCTYPE html>" in content or "<html" in content


def test_static_styles_css_accessible(client):
    """GET /static/styles.css should be accessible."""
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert "text/css" in response.headers.get("content-type", "")


def test_static_app_js_accessible(client):
    """GET /static/app.js should be accessible."""
    response = client.get("/static/app.js")
    assert response.status_code == 200
    # JavaScript file content type
    content_type = response.headers.get("content-type", "")
    assert "javascript" in content_type or "text/plain" in content_type
