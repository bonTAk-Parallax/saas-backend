
from apps.core.models import ExportJob
from apps.core.commons.dynamic_serializers import DynamicFieldsModelSerializer

class ExportJobSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ExportJob
        fields = ['id', 'status', 'file_url', 'created_at', 'completed_at']
        read_only_fields = fields
        