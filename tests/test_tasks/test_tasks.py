def test_task_list(client, auth):
    resp = client.get("/tasks/")
    assert resp.status_code == 200


def test_create_task_form(client, auth):
    resp = client.get("/tasks/new")
    assert resp.status_code == 200


def test_create_task(client, auth):
    resp = client.post("/tasks/new", data={
        "title": "My Task", "description": "Details",
        "status": "todo", "priority": "high",
        "due_date": "2026-07-01",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"My Task" in resp.data


def test_view_task(client, auth, task):
    resp = client.get(f"/tasks/{task}")
    assert resp.status_code == 200


def test_edit_task(client, auth, task):
    resp = client.post(f"/tasks/{task}/edit", data={
        "title": "Updated", "description": "Updated desc",
        "status": "done", "priority": "urgent",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Updated" in resp.data


def test_delete_task(client, auth, task):
    resp = client.post(f"/tasks/{task}/delete", data={}, follow_redirects=True)
    assert resp.status_code == 200


def test_task_requires_org(client):
    resp = client.post("/tasks/new", data={
        "title": "No org task",
    }, follow_redirects=True)
    assert b"Sign In" in resp.data


def test_dashboard_with_stats(client, auth, task):
    resp = client.get("/dashboard/")
    assert resp.status_code == 200
    assert b"Total" in resp.data


def test_export_pdf(client, auth, task):
    resp = client.get("/tasks/export/pdf")
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"
    assert len(resp.data) > 0
    assert resp.data.startswith(b"%PDF")
