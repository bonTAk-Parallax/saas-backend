
from rest_framework.permissions import BasePermission

class IsOrgMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'organization'):
            return request.user.profile.organization == obj.organization
        if hasattr(obj, 'project'):
            return request.user.profile.organization == obj.project.organization
        if hasattr(obj, 'task'):
            return request.user.profile.organization == obj.task.project.organization
        return False
    