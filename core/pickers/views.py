from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from core.tasks.models import *
from rest_framework.permissions import AllowAny
from .serializers import *
from django.core import serializers
from django.db.models import Q
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

@csrf_exempt
@api_view(['GET'])
def status_picker(request):

    data = TaskStatus.objects.all()
    serializer = StatusPickerSerializer(data, many=True)

    return Response(serializer.data, status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def permission_picker(request):

    data = TaskPermission.objects.all()
    serializer = PremissionPickerSerializer(data, many=True)

    return Response(serializer.data, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def collaborator_picker(request):

    data = User.objects.filter(is_staff=False)
    serializer = UserPickerSerializer(data, many=True)

    return Response(serializer.data, status=HTTP_200_OK)

