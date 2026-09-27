
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import Invite
from .serializers import BulkInviteCreateSerializer, InviteCreateSerializer
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
        "destroy": {"invites:create"},
        "bulk_create": {"invites:create"},
    }
    http_method_names = ["get", "post", "head"]

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk_create(self, request):
        serializer = BulkInviteCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response({
            "created": InviteCreateSerializer(result["created"], many=True).data,
            "skipped": result["skipped"],
        }, status=status.HTTP_201_CREATED)
    
