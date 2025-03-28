def create_post(client, auth_headers):
    response = client.post("/posts", json={
        "title": "Votable Post",
        "content": "Let's test votes",
        "published": True
    }, headers=auth_headers)
    return response.json()["id"]


def test_vote_post(client, auth_headers):
    post_id = create_post(client, auth_headers)

    response = client.post("/vote", json={
        "post_id": post_id,
        "direction": 1
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["message"] == "Vote registered"


def test_duplicate_vote(client, auth_headers):
    post_id = create_post(client, auth_headers)

    # First vote
    client.post("/vote", json={"post_id": post_id, "direction": 1}, headers=auth_headers)

    # Duplicate vote
    response = client.post("/vote", json={"post_id": post_id, "direction": 1}, headers=auth_headers)

    assert response.status_code == 409

def test_unvote(client, auth_headers):
    post_id = create_post(client, auth_headers)

    # Vote
    client.post("/vote", json={"post_id": post_id, "direction": 1}, headers=auth_headers)

    # Unvote
    response = client.post("/vote", json={"post_id": post_id, "direction": 0}, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["message"] == "Vote removed"


def test_unvote_without_existing_vote(client, auth_headers):
    post_id = create_post(client, auth_headers)

    response = client.post("/vote", json={"post_id": post_id, "direction": 0}, headers=auth_headers)

    assert response.status_code == 404

def test_vote_nonexistent_post(client, auth_headers):
    response = client.post("/vote", json={"post_id": 99999, "direction": 1}, headers=auth_headers)

    assert response.status_code == 404

