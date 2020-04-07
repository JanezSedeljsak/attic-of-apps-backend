from django.contrib.auth.models import User
from rest_framework import serializers
from msclone.tasks.models import Task, SubTask, TaskStatus


class TasksViewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'author']


    def get_user(self, task):
        if task.user.first_name and task.user.last_name:
            return f'{task.user.first_name} {task.user.last_name}'        
            
        return task.user.username


class TaskSerializer(TasksViewSerializer):

    time_complexity_unit = serializers.SerializerMethodField('get_complexity_unit')

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'time_complexity', 'author', 'time_complexity_unit']

    def get_complexity_unit(self, task):
        if task.time_complexity_unit:
            return task.time_complexity_unit.definition
        else:
            return None


class SubTaskSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField('get_status')
    worker = serializers.SerializerMethodField('get_user')

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status', 'worker']


    def get_status(self, stask):
        if stask.status:
            return stask.status.title
 
        return None

    def get_user(self, stask):
        if stask.done_by:
            if stask.done_by.first_name and stask.done_by.last_name:
                return f'{stask.done_by.first_name} {stask.done_by.last_name}'        
            
            return stask.done_by.username
        else:
            return None


class SubTaskDetailSerializer(SubTaskSerializer):

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status', 'worker']
