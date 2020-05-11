from django.views.generic import View
from .render import Render
from datetime import datetime
from rest_framework.status import (
    HTTP_400_BAD_REQUEST
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from core.tasks.models import *
from core.tasks.serializers import *
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.utils import timezone
from core.tasks.helpers import HelperMethods
import json


@csrf_exempt
@api_view(['GET'])
def weekly_pdf(request):
    _start = request.GET['start']
    _end = request.GET['end']

    if _start is None or _end is None:
        return Response({'error': 'Data sent was invalid'}, status=HTTP_400_BAD_REQUEST)

    datetime_start_date = datetime.strptime(_start, '%d/%m/%y')
    datetime_end_date = datetime.strptime(_end, '%d/%m/%y')

    colab_serializer = CollaboratorKeySerializer(
        TaskCollaborator.objects.filter(user=request.user), many=True)
    colabIds = [colab['task_id'] for colab in colab_serializer.data]

    tasks = Task.objects.filter((Q(pk__in=colabIds) | Q(user=request.user)) & Q(due_date__lte=datetime_end_date, due_date__gt=datetime_start_date))

    serializer = TasksViewSerializer(tasks, many=True)

    tasksWithProgress = HelperMethods.addProgressToTasks(serializer.data, fillEmpty=True)

    params = {
        'today': timezone.now(),
        'tasks': tasksWithProgress
    }

    return Render.render('brainjet_weekly_report.html', params)


@csrf_exempt
@api_view(['GET'])
def task_pdf(request):

    _task_id = request.GET['task_id']

    if _task_id is None:
        return Response({'error': 'Data sent was invalid'}, status=HTTP_400_BAD_REQUEST)

    task = Task.objects.get(pk=_task_id)
    task_serializer = TaskDetailSerializer(task)
 
    params = {
        'today': timezone.now(),
        'task': json.dumps(task_serializer.data, indent=4)
    }

    return Render.render('brainjet_task_report.html', params)
