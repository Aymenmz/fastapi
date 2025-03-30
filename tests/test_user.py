# tests/test_user.py

def test_create_user(client):
    payload = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    post = response.json()
    assert post["email"] == payload["email"]
    assert "id" in post
    assert "created_at" in post
    assert "password" not in post
