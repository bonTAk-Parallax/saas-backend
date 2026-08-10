
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.project.models import Project
from apps.task.models import Task

class Command(BaseCommand):
    help = 'Creates default groups and permissions'

    def handle(self, *args, **options):
        groups = ['ADMIN', 'MANAGER', 'MEMBER']

        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            self.stdout.write(f'{"Created" if created else "Already exists"} group: {group_name}')

        admin_group = Group.objects.get(name='ADMIN')
        manager_group = Group.objects.get(name='MANAGER')
        member_group = Group.objects.get(name='MEMBER')

        project_ct = ContentType.objects.get_for_model(Project)
        task_ct = ContentType.objects.get_for_model(Task)

        permissions = {
            'add_project': [admin_group, manager_group],
            'change_project': [admin_group, manager_group],
            'delete_project': [admin_group],
            'view_project': [admin_group, manager_group, member_group],
            'add_task': [admin_group, manager_group, member_group],
            'change_task': [admin_group, manager_group, member_group],
            'delete_task': [admin_group, manager_group],
            'view_task': [admin_group, manager_group, member_group],
        }

        for codename, groups in permissions.items():
            try:
                perm = Permission.objects.get(codename=codename)
                for group in groups:
                    group.permissions.add(perm)
                self.stdout.write(f'Assigned {codename} to specified groups')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission {codename} not found'))
