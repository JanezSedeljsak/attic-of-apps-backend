from msclone.tasks.models import Task
from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ('timestamp',)


class Message(models.Model):
    message = models.CharField(max_length=1200)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
