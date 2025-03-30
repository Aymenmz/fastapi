def test_login(client):

    payload = {
        "email": "loginuser@example.com",
        "password": "loginpass"
    }
    client.post("/users", json=payload)

    response = client.post(
        "/login",
        data={"username": payload["email"], "password": payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    post = response.json()
    assert "access_token" in post
    assert post["token_type"] == "bearer"
