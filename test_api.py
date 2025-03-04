import pytest
import requests
import logging

logger = logging.getLogger("test_project")
API_BASE = "https://test-stand.gb.ru/api/posts"

def test_create_post_and_check_existence():
    payload = {
        "title": "API Test Post",
        "description": "This is a test description for API post",
        "content": "This is the content of the API test post"
    }
    try:
        post_response = requests.post(API_BASE, json=payload)
    except Exception as e:
        logger.error("POST request error: " + str(e))
        pytest.fail("POST request failed")
    assert post_response.status_code in [200, 201], f"Unexpected status code: {post_response.status_code}"
    try:
        get_response = requests.get(API_BASE)
    except Exception as e:
        logger.error("GET request error: " + str(e))
        pytest.fail("GET request failed")
    assert get_response.status_code == 200, f"Unexpected GET status: {get_response.status_code}"
    posts = get_response.json()
    exists = any(post.get("description") == payload["description"] for post in posts)
    assert exists, "Created post not found by description"

def test_get_posts():
    try:
        response = requests.get(API_BASE)
    except Exception as e:
        logger.error("GET request error: " + str(e))
        pytest.fail("GET request failed")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
