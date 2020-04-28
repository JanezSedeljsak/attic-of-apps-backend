from django.views.generic import View
from .render import Render
from django.utils import timezone
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

    tasks = Task.objects.filter(
        (Q(pk__in=colabIds) | Q(user=request.user)) &
        Q(due_date__lte=datetime_end_date, due_date__gt=datetime_start_date)
    )

    today = timezone.now()
    params = {
        'today': today,
        'tasks': tasks,
        'user': (request.user.first_name + request.user.last_name) if request.user else '/',
        'smthn': 'kekec joža'
    }

    return Render.render('brainjet_weekly_report.html', {})


@csrf_exempt
@api_view(['GET'])
def task_pdf(request):

    _task_id = request.GET['task_id']

    if _task_id is None:
        return Response({'error': 'Data sent was invalid'}, status=HTTP_400_BAD_REQUEST)

    tasks = Task.objects.all()
    today = timezone.now()
    params = {
        'today': today,
        'tasks': tasks,
        'user': (request.user.first_name + request.user.last_name) if request.user else '/',
        'smthn': 'kekec joža'
    }

    return Render.render('brainjet_task_report.html', params)
