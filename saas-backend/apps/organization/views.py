
from .models import Invite
from .serializers import InviteCreateSerializer
from rest_framework.permissions import IsAuthenticated
from apps.core.commons.mixins import TenantAwareMixin
from rest_framework import viewsets
from apps.core.permissions.permissions import HasTenantAccess, HasScope


class InviteViewSet(TenantAwareMixin, viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteCreateSerializer
    permission_classes = [IsAuthenticated, HasTenantAccess, HasScope]
    required_scopes = {
        "list": {"invites:read"},
        "create": {"invites:create"},
    }
    http_method_names = ["get", "post", "head"]

