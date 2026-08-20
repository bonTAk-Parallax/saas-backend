
from django.db import transaction
from apps.core.commons.middlewares.request_id import get_request_id
from apps.core.models.audit_log import AuditLog


def create_task(*, user, project, title, description="", assigned_to=None, due_date=None, is_done=False):
    with transaction.atomic():
        task = Task.objects.create(
            project=project, title=title, description=description,
            assigned_to=assigned_to, due_date=due_date, is_done=is_done,
            created_by=user,
        )
        AuditLog.objects.create(
            organization=project.organization, actor=user, action='CREATE',
            model_name='Task', object_id=str(task.id), request_id=get_request_id(),
        )
    return task


def delete_task(*, user, task):
    with transaction.atomic():
        task.delete()  
        AuditLog.objects.create(
            organization=task.project.organization, actor=user, action='DELETE',
            model_name='Task', object_id=str(task.id), request_id=get_request_id(),
        )
        