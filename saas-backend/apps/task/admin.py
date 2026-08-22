from django.contrib import admin
from apps.task.models.task import Task
from apps.task.models.comments import Comment

admin.site.register(Task)
admin.site.register(Comment)

