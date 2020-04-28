from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmailConf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=100)
    fallback = models.TextField()
    type = models.CharField(max_length=100, default="confirm")
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('timestamp',)