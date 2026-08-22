
from django.db import transaction
from django.utils.timezone import now
from apps.core.models.audit_log import AuditLog
from apps.core.models.export import ExportJob
from apps.core.queue.queue_client import queue_task
from apps.core.commons.middlewares.request_id import get_request_id
from apps.project.models import Project

def create_project(*, organization, user, title, description=""):
    with transaction.atomic():
        project = Project.objects.create(
            organization=organization, title=title, description=description, created_by=user,
        )
        AuditLog.objects.create(
            organization=organization, actor=user, action='CREATE',
            model_name='Project', object_id=str(project.id),
            changes={'title': [None, title]}, request_id=get_request_id(),
        )
    return project


def create_export_job(*, organization, user):
    with transaction.atomic():
        export_job = ExportJob.objects.create(
            organization=organization,
            status=ExportJob.Status.PENDING,
            job_id=None, 
        )
        AuditLog.objects.create(
            organization=organization, actor=user, action='CREATE',
            model_name='ExportJob', object_id=str(export_job.id),
            request_id=get_request_id(),
        )
        transaction.on_commit(
            lambda: _enqueue_export(export_job.id, get_request_id())
        )
    return export_job


def _enqueue_export(export_job_id, request_id):
    job = queue_task(
        'apps.project.tasks.generate_export',
        str(export_job_id), request_id,
    )
    ExportJob.objects.filter(id=export_job_id).update(job_id=job.id)


def mark_export_completed(export_job_id, file_url):
    with transaction.atomic():
        export_job = (
            ExportJob.objects
            .select_for_update()
            .get(id=export_job_id)
        )

        export_job.status = ExportJob.Status.COMPLETED
        export_job.file_url = file_url
        export_job.completed_at = now()

        export_job.save(
            update_fields=[
                "status",
                "file_url",
                "completed_at",
                "updated_at",
            ]
        )
        
