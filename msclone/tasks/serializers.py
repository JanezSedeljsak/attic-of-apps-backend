from django.contrib.auth.models import User
from rest_framework import serializers
from msclone.tasks.models import Task, SubTask, TaskStatus, TaskCollaborators


class TasksViewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'author']


    def get_user(self, task):

        if hasattr(task, "user"):
            if task.user.first_name and task.user.last_name:
                return f'{task.user.first_name} {task.user.last_name}'        
            
        return None





class SubTaskSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField('get_status')
    worker = serializers.SerializerMethodField('get_user')

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status', 'worker']


    def get_status(self, stask):

        if hasattr(stask, "status"):
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

class TaskCollaboratorSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField('get_user')
    
    class Meta:
        model = TaskCollaborators
        fields = ['timestamp', 'user']


    def get_user(self, collaborator):
        if hasattr(collaborator, "user"):  
            if collaborator.user.first_name and collaborator.user.last_name:
                return f'{collaborator.user.first_name} {collaborator.user.last_name}'  
        else:
            return None

class TaskSerializer(TasksViewSerializer):

    subtasks = SubTaskSerializer(many=True)
    collaborators = TaskCollaboratorSerializer(many=True, source='taskcollaboratorss')
    time_complexity_unit = serializers.SerializerMethodField('get_complexity_unit')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'time_complexity', 
            'author', 'time_complexity_unit', 'subtasks', 'collaborators']

    def get_complexity_unit(self, task):

        if hasattr(task, "time_complexity_unit"):
            return task.time_complexity_unit.definition

        return None


class SubTaskDetailSerializer(SubTaskSerializer):

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status', 'worker']