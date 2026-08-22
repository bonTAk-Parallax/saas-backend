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
    def has_permission(self, request, view):
        required_map = getattr(view, "required_scopes", {})
        
        if isinstance(required_map, dict):
            required = required_map.get(view.action, set())
        else:
            required = required_map

        if not required:
            return True

        profile = getattr(request.user, "profile", None)
        if profile is None:
            return False

        user_scopes = ROLE_SCOPES.get(profile.role, set())
        return required.issubset(user_scopes)
    