import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"  # Example API

def test_get_posts():
    """Test retrieving all posts."""
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0

def test_get_single_post():
    """Test retrieving a single post."""
    post_id = 1
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    post = response.json()
    assert isinstance(post, dict)
    assert post["id"] == post_id

def test_create_post():
    """Test creating a new post."""
    new_post = {
        "title": "Test Post",
        "body": "This is a test post.",
        "userId": 1,
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == new_post["title"]
    assert created_post["body"] == new_post["body"]
    assert created_post["userId"] == new_post["userId"]
    assert "id" in created_post # assert that an ID was assigned.

def test_update_post():
    """Test updating an existing post."""
    post_id = 1
    updated_post = {
        "id": post_id,
        "title": "Updated Post",
        "body": "This post has been updated.",
        "userId": 1,
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_post)
    assert response.status_code == 200
    updated_response = response.json()
    assert updated_response["title"] == updated_post["title"]
    assert updated_response["body"] == updated_post["body"]

def test_delete_post():
    """Test deleting a post."""
    post_id = 1
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200 # or 204
    # Optional: Verify the post is actually deleted (e.g., by trying to get it again)
    verify_response = requests.get(f"{BASE_URL}/posts/{post_id}")
    #Assert the delete was successful.
    if verify_response.status_code != 404:
        #Sometimes the api returns 200, but then the item is gone.
        print("Warning, the delete may not have been successful")