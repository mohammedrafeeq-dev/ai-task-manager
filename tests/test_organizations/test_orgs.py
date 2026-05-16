def test_create_org_page(client, auth):
    resp = client.get("/org/settings")
    assert resp.status_code == 200


def test_create_org_duplicate_slug(client):
    # Create first user with org
    client.post("/auth/register", data={
        "name": "User1", "email": "u1@test.com",
        "password": "password123", "confirm": "password123",
    })
    client.post("/org/create", data={
        "name": "Org1", "slug": "testslug",
    })
    client.get("/auth/logout")
    # New user tries same slug
    client.post("/auth/register", data={
        "name": "User2", "email": "u2@test.com",
        "password": "password123", "confirm": "password123",
    })
    resp = client.post("/org/create", data={
        "name": "Org2", "slug": "testslug",
    })
    assert b"already taken" in resp.data


def test_org_redirect_when_no_org(client):
    resp = client.get("/org/settings", follow_redirects=True)
    assert b"Sign In" in resp.data
