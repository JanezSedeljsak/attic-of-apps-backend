from django.contrib.auth.models import User
from rest_framework import serializers
from msclone.tasks.models import *
from datetime import *
from rest_framework.fields import CurrentUserDefault

class CollaboratorKeySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TaskCollaborator
        fields = ['task_id']

class SubTaskProgressSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ['id', 'status_id']

class TasksViewSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField('get_user')
    subtasks = SubTaskProgressSerilaizer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'author', 'subtasks', 'is_event']

    def get_user(self, task):

        if hasattr(task, "user"):
            if task.user.first_name and task.user.last_name:
                return f'{task.user.first_name} {task.user.last_name}'

        return None

class TaskCalendarViewSerailizer(TasksViewSerializer):
    
    name = serializers.CharField(source='title')
    start = serializers.DateTimeField(source='due_date', format="%Y-%m-%d %H:%M")
    subtasks = SubTaskProgressSerilaizer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'start', 'name', 'author', 'user_id', 'subtasks', 'time_complexity', 'is_event']



class SubTaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status_id']

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class SubTaskFormSerializer(serializers.ModelSerializer):

    # status = serializers.SerializerMethodField('get_status')
    # worker = serializers.SerializerMethodField('get_user')

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status_id', 'done_date']


class CollaboratorFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskCollaborator
        fields = ['permission_id', 'user_id']

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class TaskFormSerializer(TasksViewSerializer):

    subtasks = SubTaskFormSerializer(many=True)
    collaborators = CollaboratorFormSerializer(
        many=True, source='taskcollaborators')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'time_complexity',
                  'user_id', 'subtasks', 'collaborators', 'timestamp', 'is_event']

    def create(self, validated_data):
        subtasks = validated_data.pop('subtasks') or []
        collaborators = validated_data.pop('taskcollaborators') or []

        task = Task.objects.create(**validated_data)

        for subtask in subtasks:
            SubTask.objects.create(**subtask, task=task)
        
        for collaborator in collaborators:
            TaskCollaborator.objects.create(**collaborator, task=task)

        return task

    def update(self, instance, validated_data):
        subtasks = validated_data.pop('subtasks') or []
        collaborators = validated_data.pop('taskcollaborators') or []

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class SubTaskDetailSerializer(SubTaskFormSerializer):

    status = serializers.SerializerMethodField('get_status')
    worker = serializers.SerializerMethodField('get_user')

    class Meta:
        model = SubTask
        fields = ['title', 'status', 'worker', 'done_date', 'status_id']

    def get_status(self, stask):

        if hasattr(stask, "status"):
            if bool(stask.status):
                return stask.status.title

        return None

    def get_user(self, stask):
        if hasattr(stask, "done_by"):
            if stask.done_by:
                if stask.done_by.first_name and stask.done_by.last_name:
                    return f'{stask.done_by.first_name} {stask.done_by.last_name}'

                return stask.done_by.username
        else:
            return None


class CollaboratorDetailSerializer(serializers.ModelSerializer):

    permissions = serializers.SerializerMethodField('get_permission')
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = TaskCollaborator
        fields = ['permissions', 'user']

    def get_permission(self, colab):

        if hasattr(colab, "permission"):
            if bool(colab.permission):
                return colab.permission.title

        return None

    def get_user(self, colab):
        if hasattr(colab, "user"):
            if colab.user:
                if colab.user.first_name and colab.user.last_name:
                    return f'{colab.user.first_name} {colab.user.last_name}'

                return colab.user.username
        else:
            return None


class TaskDetailSerializer(TasksViewSerializer):

    subtasks = SubTaskDetailSerializer(many=True)
    collaborators = CollaboratorDetailSerializer(
        many=True, source='taskcollaborators')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'time_complexity',
                  'author', 'subtasks', 'collaborators', 'timestamp', 'is_event']
