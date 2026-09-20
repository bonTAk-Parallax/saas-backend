import pytest
from apps.project.models import Project  


@pytest.mark.django_db
def test_user_cannot_see_other_org_projects_in_list(auth_client, other_org):
    """
    auth_client and other_org both come from conftest.py — auth_client is
    already logged in as an ADMIN in `org`. This test never mentions
    "org" directly because auth_client's fixture chain already created it.
    """
    Project.objects.create(organization=other_org, title="Beta Secret Project")

    response = auth_client.get("/api/v1/projects/")
    titles = [p["title"] for p in response.data]

    assert "Beta Secret Project" not in titles


@pytest.mark.django_db
def test_user_cannot_retrieve_other_org_project_directly(auth_client, other_org):
    """
    Even knowing the exact ID, a user outside the org shouldn't be able
    to fetch it directly — this is what HasTenantAccess's object-level
    check exists for specifically.
    """
    project = Project.objects.create(organization=other_org, title="Beta Secret Project")

    response = auth_client.get(f"/api/v1/projects/{project.id}/")

    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_user_can_see_own_org_projects(auth_client, org):
    Project.objects.create(organization=org, title="My Own Project")

    response = auth_client.get("/api/v1/projects/")
    titles = [p["title"] for p in response.data]

    assert "My Own Project" in titles


@pytest.mark.django_db
def test_cannot_create_task_under_other_orgs_project(auth_client, other_org):
    """
    Tests TenantAwareModelSerializer's validate() — a write that
    references a related object from a different org should be rejected
    at validation, not silently succeed.
    """
    project = Project.objects.create(organization=other_org, title="Beta Project")

    response = auth_client.post("/api/v1/tasks/", {
        "project": str(project.id),
        "title": "Sneaky cross-org task",
    })

    assert response.status_code == 400