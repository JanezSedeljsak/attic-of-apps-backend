from django.contrib.auth.models import User
from rest_framework import serializers
from msclone.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
