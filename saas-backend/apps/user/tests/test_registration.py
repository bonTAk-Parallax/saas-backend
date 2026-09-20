import pytest
from apps.user.services import register_user  
from apps.user.api.v1.serializers import UserRegistrationSerializer  # adjust import


@pytest.mark.django_db
def test_register_user_creates_org_and_profile():
    user = register_user(
        username="newadmin",
        email="newadmin@example.com",
        password="testpass123",
        organization_name="New Company",
    )

    assert user.profile is not None
    assert user.profile.organization.name == "New Company"
    assert user.profile.role == "ADMIN"


@pytest.mark.django_db
def test_registration_rejects_duplicate_email(org):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_user(username="existing", email="dupe@example.com", password="x")

    serializer = UserRegistrationSerializer(data={
        "username": "someoneelse",
        "email": "dupe@example.com",
        "password": "testpass123",
        "organization_name": "Whatever Co",
    })

    assert not serializer.is_valid()
    assert "email" in serializer.errors
