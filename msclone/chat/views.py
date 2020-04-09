from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from .models import Message, Chat
from rest_framework.permissions import AllowAny
from .serializers import MessageSerializer, ChatSerializer
from django.core import serializers
from django.db.models import Q
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)


@csrf_exempt
@api_view(['POST'])
def send_message(request, chat_id):
    message_skeleton = Message(sender=request.user)
    message_serializer = MessageSerializer(message_skeleton, data=request.data)
    if message_serializer.is_valid():
        message_serializer.save()
        return Response(message_serializer.data, status=HTTP_201_CREATED)
    return Response(message_serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def update_message(request, message_id):
    result = {}

    if not Message.objects.filter(id=message_id).exists():
        return Response({'error': 'The message you are looking for does not exist'}, status=HTTP_404_NOT_FOUND) 

    message = Message.objects.get(id=message_id)

    if request.method == 'PUT':
        message_serializer = MessageSerializer(message, data=request.data)
        if message_serializer.is_valid():
            message_serializer.save()
            result['success'] = True
        else:
            return Response({'error': message_serializer.errors}, status=HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE':
        operation = message.delete()
        result['success'] = bool(operation)

    return Response(result, status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_all_messages(request, task_id):

    messages = Message.objects.filter(task_id=task_id)
    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data, status=HTTP_200_OK)