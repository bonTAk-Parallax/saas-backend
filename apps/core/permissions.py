from rest_framework.permissions import BasePermission
from .roles import ROLE_SCOPES

class HasTenantAccess(BasePermission):
    """Allow access only when the object belongs to the user's organization."""
    def has_object_permission(self, request, view, obj):
        profile = getattr(request.user, "profile", None)
        if profile is None or not hasattr(obj, "resolve_tenant"):
            return False
        return obj.resolve_tenant() == profile.organization


class HasScope(BasePermission):
    """Allow access when the user's role has the required scope."""

    def has_permission(self, request, view):
        required = getattr(view, "required_scopes", set())
        if not required:
            return True
        
        profile = getattr(request.user, "profile", None)
        if profile is None:
            return False
        
        user_scopes = ROLE_SCOPES.get(profile.role, set())
        return required.issubset(user_scopes)
    