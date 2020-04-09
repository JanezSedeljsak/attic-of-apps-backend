from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class TaskUnits(models.Model):
    definition = models.CharField(max_length=30)
    longname =  models.TextField(blank=True, default=None)

    def __str__(self):
        return self.definition

    class Meta:
        ordering = ('definition',)

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    due_date = models.DateTimeField()
    time_complexity = models.IntegerField(blank=True, default=0)
    time_complexity_unit = models.ForeignKey(TaskUnits, blank=True, default=None, on_delete=models.CASCADE)

    @property
    def subtasks(self):
        return self.subtask_set.all()

    @property
    def taskcollaboratorss(self):
        return self.taskcollaborators_set.all()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('timestamp',)


class TaskCollaborators(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.user.get_username()

    class Meta:
        ordering = ('timestamp',)

class TaskStatus(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)



class SubTask(models.Model):
    title = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, null=True)
    done_date = models.DateTimeField(blank=True, null=True)
    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('status', 'timestamp')