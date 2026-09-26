import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.organization.models import Organization
from apps.user.models.user_profile import UserProfile

User = get_user_model()


@pytest.fixture
def org(db):
    """
    A fresh Organization for this test only.
    The `db` parameter here is pytest-django's built-in fixture — just
    listing it as a parameter is what grants this test database access.
    Without it, any ORM call in a test raises an error on purpose — a
    guardrail so tests can't silently touch the database by accident.
    """
    return Organization.objects.create(name="Alpha")


@pytest.fixture
def other_org(db):
    """A second, separate organization — for proving isolation between them."""
    return Organization.objects.create(name="Beta")


@pytest.fixture
def make_user(db):
    """
    A FACTORY fixture — instead of returning one object, it returns a
    FUNCTION that makes objects, so each test can call it as many times
    as it needs with different arguments. This is the pytest equivalent
    of a helper method you'd otherwise write per test class.
    """
    def _make(email, organization, role="MEMBER"):
        user = User.objects.create_user(
            username=email, email=email, password="testpass123"
        )
        UserProfile.objects.create(user=user, organization=organization, role=role)
        return user
    return _make


@pytest.fixture
def api_client():
    """A plain, unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture
def admin_user(make_user, org):
    return make_user("admin@alpha.test", org, role="ADMIN")


@pytest.fixture
def member_user(make_user, org):
    return make_user("member@alpha.test", org, role="MEMBER")


@pytest.fixture
def auth_client(api_client, admin_user):
    """
    An APIClient already authenticated as admin_user.
    force_authenticate bypasses actually calling the login endpoint and
    getting a real JWT — appropriate here because these tests are about
    permission/isolation logic, not the login flow itself (that gets its
    own dedicated test, see test_registration.py).
    """
    api_client.force_authenticate(user=admin_user)
    return api_client