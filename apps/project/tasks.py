
import csv
import os
from django.conf import settings
from django.utils.timezone import now
from apps.project.models import Project
from apps.core.models.export import ExportJob
from django_rq import job

@job
def generate_export(org_id):
    try:
        projects = Project.objects.filter(organization_id=org_id).prefetch_related('tasks')
        filename = f"export_{org_id}_{now().timestamp()}.csv"
        filepath = os.path.join(settings.MEDIA_ROOT, 'exports', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Project Title', 'Task Title', 'Is Done', 'Assigned To'])
            for project in projects:
                for task in project.tasks.all():
                    writer.writerow([project.title, task.title, task.is_done, task.assigned_to.username if task.assigned_to else ''])

        file_url = f"/media/exports/{filename}"
        export_job = ExportJob.objects.get(job_id=job.id)
        export_job.status = 'COMPLETED'
        export_job.file_url = file_url
        export_job.completed_at = now()
        export_job.save()
    except Exception as e:
        export_job = ExportJob.objects.get(job_id=job.id)
        export_job.status = 'FAILED'
        export_job.save()
        raise e
    