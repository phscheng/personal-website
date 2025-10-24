def test_projects_page_shows_no_projects_initially(client):
    """When DB is empty, the projects page should show the 'No projects found' message."""
    resp = client.get("/projects")
    assert resp.status_code == 200
    assert b"No projects found. Use the form below to add your first project!" in resp.data


def test_add_project_and_listed_on_page(client):
    """POSTing a valid project should add it to the DB and then appear on the projects page."""
    data = {
        "project_title": "Test Project",
        "project_description": "This is a test project description.",
        "project_image": "test.jpg",
    }

    # Submit the form and follow redirect
    resp = client.post("/projects", data=data, follow_redirects=True)
    assert resp.status_code == 200

    # The page should contain the success flash (if present) and the new project
    assert b"Test Project" in resp.data
    assert b"This is a test project description." in resp.data
