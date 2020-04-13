from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class TaskPermission(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, default="", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

class TaskUnit(models.Model):
    definition = models.CharField(max_length=30)
    longname =  models.TextField(null=True, default="", blank=True)

    def __str__(self):
        return self.definition

    class Meta:
        ordering = ('definition',)

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(default="", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    time_complexity = models.IntegerField(default=0)
    time_complexity_unit = models.ForeignKey(TaskUnit, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def subtasks(self):
        return self.subtask_set.all()

    @property
    def taskcollaborators(self):
        return self.taskcollaborator_set.all()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('timestamp',)


class TaskCollaborator(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    permission = models.ForeignKey(TaskPermission, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_username()

    class Meta:
        ordering = ('timestamp',)

class TaskStatus(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, default="", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('pk',)



class SubTask(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, default="", blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, null=True, blank=True)
    done_date = models.DateTimeField(null=True, blank=True)
    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('status', 'timestamp')