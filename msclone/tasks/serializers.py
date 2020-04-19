from django.contrib.auth.models import User
from rest_framework import serializers
from msclone.tasks.models import *

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


class SubTaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status_id']

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class SubTaskSerializer(serializers.ModelSerializer):

    #status = serializers.SerializerMethodField('get_status')
    #worker = serializers.SerializerMethodField('get_user')

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status_id', 'done_date']


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

class TaskCollaboratorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TaskCollaborator
        fields = ['permission_id', 'user_id']

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

class TaskSerializer(TasksViewSerializer):

    subtasks = SubTaskSerializer(many=True)
    collaborators = TaskCollaboratorSerializer(many=True, source='taskcollaborators')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'time_complexity', 
            'user_id', 'subtasks', 'collaborators', 'timestamp']

    def update(self, instance, validated_data):
        subtasks = validated_data.pop('subtasks') or []
        collaborators = validated_data.pop('taskcollaborators') or []
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        updated_subtask_ids = set([s['id'] for s in subtasks if 'id' in s])
        subtask_ids_to_delete = [s.id for s in instance.subtasks if s.id not in updated_subtask_ids]

        for subtask_id in subtask_ids_to_delete:
            SubTask.objects.filter(id=subtask_id).delete()

        for subtask in subtasks:
            subtask_skeleton = SubTask(task=instance)
            subtask_serializer = SubTaskUpdateSerializer(subtask_skeleton, data=subtask)
            if subtask_serializer.is_valid():
                subtask_serializer.save()

        updated_collaborator_ids = set([s['id'] for s in collaborators if 'id' in s])
        collaborator_ids_to_delete = [s.id for s in instance.taskcollaborators if s.id not in updated_collaborator_ids]

        for collab_id in collaborator_ids_to_delete:
            TaskCollaborator.objects.filter(id=collab_id).delete()

        return instance



class SubTaskDetailSerializer(SubTaskSerializer):

    class Meta:
        model = SubTask
        fields = ['title', 'done_by', 'status', 'worker', 'done_date']
