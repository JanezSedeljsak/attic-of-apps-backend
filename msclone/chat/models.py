from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Chat(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('timestamp',)


class Message(models.Model):
    message = models.CharField(max_length=1200)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
