from django.conf import settings
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    due_date = models.DateTimeField(auto_now=True)


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    index = models.IntegerField()
    done = models.BooleanField(default=False)
    done_date = models.DateTimeField(blank=True, null=True)
    done_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, blank=True, null=True)