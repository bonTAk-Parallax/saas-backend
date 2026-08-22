from django.contrib import admin
from apps.core.models.export import ExportJob
from apps.core.models.audit_log import AuditLog

admin.site.register(ExportJob)
admin.site.register(AuditLog)

