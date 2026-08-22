
import csv
import os
import logging
from django.utils.timezone import now
import django_rq
from django_rq import job
from rq import get_current_job
from apps.core.models.export import ExportJob
from apps.project.models import Project
from apps.project.services.export import mark_export_completed
from django.conf import settings

logger = logging.getLogger(__name__)

@job('default')
def generate_export(export_job_id, request_id=""):
    current_job = get_current_job()
    log = logging.LoggerAdapter(logger, {'request_id': request_id})

    try:
        export_job = ExportJob.objects.select_related('organization').get(id=export_job_id)
        projects = Project.objects.filter(
            organization_id=export_job.organization_id
        ).prefetch_related('tasks')

        filename = f"export_{export_job.organization_id}_{now().timestamp()}.csv"
        filepath = os.path.join(settings.MEDIA_ROOT, 'exports', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Project Title', 'Task Title', 'Is Done', 'Assigned To'])
            for project in projects:
                for task in project.tasks.all():
                    writer.writerow([
                        project.title, task.title, task.is_done,
                        task.assigned_to.username if task.assigned_to else '',
                    ])

        mark_export_completed(export_job_id, f"/media/exports/{filename}")

    except Exception as exc:
        log.error("Export job %s failed: %s", export_job_id, exc, exc_info=True)
        if current_job and current_job.retries_left == 0:
            ExportJob.objects.filter(id=export_job_id).update(status=ExportJob.Status.FAILED)
        raise
    