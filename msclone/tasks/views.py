from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from msclone.tasks.models import Task
from rest_framework.permissions import AllowAny
from msclone.tasks.serializers import TaskSerializer
from django.core import serializers
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_task(request, task_id):

    if not Task.objects.filter(id=task_id).exists():
        return Response({'error': 'The task you are searching for does not exist'}, status=HTTP_404_NOT_FOUND) 
        
    task = Task.objects.get(id=task_id)
    serializer = TaskSerializer(task)

    return Response(serializer.data, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_all_tasks(request):

    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data, status=HTTP_200_OK)
        

    