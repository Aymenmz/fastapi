def test_login(client):
    # First, register the user with JSON
    payload = {
        "email": "loginuser@example.com",
        "password": "loginpass"
    }
    client.post("/users", json=payload)

    # Then, login with FORM data
    response = client.post(
        "/login",
        data={"username": payload["email"], "password": payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    post = response.json()
    assert "access_token" in post
    assert post["token_type"] == "bearer"
