def test_create_post(client, auth_headers):
    payload = {
        "title": "Test Post",
        "content": "Test content",
        "published": True
    }

    response = client.post("/posts", json=payload, headers=auth_headers)

    assert response.status_code == 201
    post = response.json()
    assert post["title"] == payload["title"]
    assert post["content"] == payload["content"]
    assert post["published"] is True


def test_get_posts(client, auth_headers):
    # Create a post first
    client.post("/posts", json={
        "title": "Another Post",
        "content": "Some content",
        "published": False
    }, headers=auth_headers)

    # Now fetch all posts
    response = client.get("/posts", headers=auth_headers)

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) >= 1


def test_get_post_by_id(client, auth_headers):
    # Create a post
    response = client.post("/posts", json={
        "title": "Get Post",
        "content": "Post Content",
        "published": True
    }, headers=auth_headers)
    post_id = response.json()["id"]

    # Fetch it back
    response = client.get(f"/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == post_id
    assert post["title"] == "Get Post"


def test_update_post(client, auth_headers):
    # Create a post
    response = client.post("/posts", json={
        "title": "Old Title",
        "content": "Old Content",
        "published": True
    }, headers=auth_headers)
    post_id = response.json()["id"]

    # Update the post
    updated_data = {
        "title": "New Title",
        "content": "New Content",
        "published": False
    }
    response = client.put(f"/posts/{post_id}", json=updated_data, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_post(client, auth_headers):
    # Create a post
    response = client.post("/posts", json={
        "title": "Delete Me",
        "content": "I will be gone",
        "published": True
    }, headers=auth_headers)
    post_id = response.json()["id"]

    # Delete the post
    response = client.delete(f"/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 204

    # Try to get it again
    response = client.get(f"/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 404



