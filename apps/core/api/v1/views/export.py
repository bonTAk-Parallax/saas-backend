
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.api.v1.serializers.export import ExportJobSerializer
from apps.core.commons.mixins import TenantAwareMixin
from apps.core.models.export import ExportJob
from apps.core.permissions.permissions import HasTenantAccess  

class ExportJobViewSet(TenantAwareMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ExportJob.objects.all()
    serializer_class = ExportJobSerializer
    permission_classes = [IsAuthenticated, HasTenantAccess]

