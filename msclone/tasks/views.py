from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from msclone.tasks.models import *
from rest_framework.permissions import AllowAny
from msclone.tasks.serializers import *
from django.core import serializers
from django.db.models import Q
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def get_task(request, task_id):

    result = {}

    if not Task.objects.filter(id=task_id).exists():
        return Response({'error': 'The task you are searching for does not exist'}, status=HTTP_404_NOT_FOUND) 

    task = Task.objects.get(id=task_id)

    if request.method == 'GET':   
        task_serializer = TaskSerializer(task)
        result = task_serializer.data


    elif request.method == 'PUT':
        task_serializer = TaskSerializer(task, data=request.data)
        if task_serializer.is_valid():
            task_serializer.save()
            result['success'] = True
        else:
            return Response({'error': task_serializer.errors}, status=HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE':
        operation = task.delete()
        result['success'] = bool(operation)


    return Response(result, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def create_task(request):
    task_skeleton = Task(user=request.user)
    task_serializer = TaskSerializer(task_skeleton, data=request.data)
    if task_serializer.is_valid():
        task_serializer.save()
        return Response(task_serializer.data, status=HTTP_201_CREATED)
    return Response(task_serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def get_all_tasks(request):

    tasks = Task.objects.all()
    serializer = TasksViewSerializer(tasks, many=True)

    return Response(serializer.data, status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_sub_task(request, task_id, subtask_id):

    if not SubTask.objects.filter(Q(id=subtask_id) & Q(task_id=task_id)).exists():
        return Response({'error': 'The sub task you are searching for does not exist'}, status=HTTP_404_NOT_FOUND) 
        
    subtask = SubTask.objects.get(id=subtask_id)
    subtask_serializer = SubTaskSerializer(subtask)
    

    return Response(subtask_serializer.data, status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_your_tasks_for_daterange(request, start_date, end_date):

    # @ FORMAT EXAMPLE: '09/19/18-13:55:26'

    datetime_start_date = datetime.strptime(start_date, '%m/%d/%y-%H:%M:%S')
    datetime_end_date = datetime.strptime(end_date, '%m/%d/%y-%H:%M:%S')

    tasks = Task.objects.filter(
        Q(user=request.user) & 
        Q(timestamp__lte=datetime_start_date, timestamp__gt=datetime_end_date)
    )
    task_serializer = TasksViewSerializer(tasks, many=True)

    return Response(task_serializer.data, status=HTTP_200_OK)



        

    