from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('timestamp',)


class SubTask(models.Model):
    title = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    index = models.IntegerField()
    done = models.BooleanField(default=False)
    done_date = models.DateTimeField(blank=True, null=True)
    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('index',)