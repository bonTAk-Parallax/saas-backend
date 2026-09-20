
import pytest
from unittest.mock import Mock
from apps.core.permissions.permissions import HasScope, ROLE_SCOPES


class FakeView:
    """
    A minimal stand-in for a real DRF view — HasScope only ever reads
    `.action` and `.required_scopes` off the view, so we don't need a
    real ProjectViewSet or a live HTTP request to test its logic. This
    is what makes this a genuine UNIT test rather than an integration
    test — fast, no database, no network.
    """
    def __init__(self, action, required_scopes):
        self.action = action
        self.required_scopes = required_scopes


def make_request(role):
    request = Mock()
    request.user.profile.role = role
    return request


@pytest.mark.parametrize("role,expected", [
    ("ADMIN", True),
    ("MANAGER", True),
    ("MEMBER", True),
])
def test_read_allowed_for_every_role(role, expected):
    """
    Regression test for the bug already found before and
    fixed once — ROLE_MATRIX originally had no 'read' scope for ANY
    role, so this test would have failed loudly before that fix, instead
    of surfacing as a confusing 403 discovered by hand three debugging
    sessions later.
    """
    view = FakeView(action="list", required_scopes={"list": {"projects:read"}})
    request = make_request(role)

    result = HasScope().has_permission(request, view)

    assert result == expected


def test_write_denied_for_member():
    view = FakeView(action="create", required_scopes={"create": {"projects:write"}})
    request = make_request("MEMBER")

    assert HasScope().has_permission(request, view) is False


def test_delete_only_allowed_for_admin():
    view = FakeView(action="destroy", required_scopes={"destroy": {"projects:delete"}})

    assert HasScope().has_permission(make_request("ADMIN"), view) is True
    assert HasScope().has_permission(make_request("MANAGER"), view) is False
    assert HasScope().has_permission(make_request("MEMBER"), view) is False


def test_action_with_no_required_scopes_is_open():
    """If a view.action isn't in required_scopes at all, access defaults to allowed."""
    view = FakeView(action="health_check", required_scopes={})
    request = make_request("MEMBER")

    assert HasScope().has_permission(request, view) is True


def test_no_profile_denies_access():
    view = FakeView(action="list", required_scopes={"list": {"projects:read"}})
    request = Mock()
    request.user.profile = None

    assert HasScope().has_permission(request, view) is False


def test_every_role_in_matrix_can_read_projects():
    """
    Sanity check directly on ROLE_SCOPES itself, not through the
    permission class — catches the exact class of bug from before
    (an entire resource:action pair silently missing from the matrix)
    without needing a fake request at all.
    """
    for role in ("ADMIN", "MANAGER", "MEMBER"):
        assert "projects:read" in ROLE_SCOPES.get(role, set()), (
            f"{role} is missing projects:read — check ROLE_MATRIX"
        )
