def test_login_page_loads(client):
    resp = client.get("/auth/login")
    assert resp.status_code == 200


def test_register_page_loads(client):
    resp = client.get("/auth/register")
    assert resp.status_code == 200


def test_register_and_login(client):
    resp = client.post("/auth/register", data={
        "name": "Alice", "email": "alice@example.com",
        "password": "secret123", "confirm": "secret123",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Create Your Organization" in resp.data


def test_register_duplicate_email(client):
    client.post("/auth/register", data={
        "name": "A", "email": "dup@example.com",
        "password": "secret123", "confirm": "secret123",
    })
    resp = client.post("/auth/register", data={
        "name": "B", "email": "dup@example.com",
        "password": "secret123", "confirm": "secret123",
    })
    assert b"already registered" in resp.data


def test_login_redirect(client):
    client.post("/auth/register", data={
        "name": "Bob", "email": "bob@example.com",
        "password": "secret123", "confirm": "secret123",
    })
    resp = client.post("/auth/login", data={
        "email": "bob@example.com", "password": "secret123",
    }, follow_redirects=True)
    assert resp.status_code == 200


def test_logout(client, auth):
    resp = client.get("/auth/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Sign In" in resp.data


def test_login_required(client):
    resp = client.get("/tasks/", follow_redirects=True)
    assert b"Sign In" in resp.data
