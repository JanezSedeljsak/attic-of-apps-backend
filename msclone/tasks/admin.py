from django.contrib import admin

# Register your models here.
from .models import Task, SubTask, TaskCollaborators, TaskStatus, TaskUnits

admin.site.register([Task, SubTask, TaskCollaborators, TaskStatus, TaskUnits])