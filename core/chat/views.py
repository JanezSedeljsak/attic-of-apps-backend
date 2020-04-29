from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from .models import Message, Chat
from rest_framework.permissions import AllowAny
from .serializers import MessageSerializer, ChatSerializer, MessageCreateSerializer
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
def send_message(request, task_id):

    if request.data.get('message') is None:
        return Response({'error': "You can't send empty message"}, status=HTTP_400_BAD_REQUEST) 

    if not Chat.objects.filter(task=task_id).exists():
        return Response({'error': "The chat doesn't exist"}, status=HTTP_404_NOT_FOUND) 

    chat = Chat.objects.get(task=task_id)

    data = { "sender": request.user.id, "chat": chat.id }
    data.update(request.data)


    message_serializer = MessageCreateSerializer(data=data)
    if not message_serializer.is_valid():
        return Response({'error': message_serializer.errors}, status=HTTP_400_BAD_REQUEST) 

    message_serializer.save()
    return Response({'ok': True }, status=HTTP_200_OK) 

@csrf_exempt
@api_view(['GET'])
def get_or_create_chat(request, task_id):

    chat = None

    if not Chat.objects.filter(task=task_id).exists():
        chat = Chat.objects.create(task_id=task_id)
    else:
        chat = Chat.objects.get(task=task_id)

    messeges = Message.objects.filter(chat=chat.id).order_by('-timestamp')

    messege_serializer = MessageSerializer(messeges, many=True)

    return Response(messege_serializer.data, status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def get_new_messages(request, task_id):

    if not request.data.get('count'):
        if not request.data.get('isZero'):
            return Response({'error': "Invalid request"}, status=HTTP_400_BAD_REQUEST)

    if not Chat.objects.filter(task=task_id).exists():
        return Response({'error': "The chat doesn't exist"}, status=HTTP_404_NOT_FOUND) 

    chat = Chat.objects.get(task=task_id)

    count = request.data['count']
    current_message_count = Message.objects.filter(chat=chat.id).count()

    new_amount = (current_message_count - count)

    if new_amount == 0:
        # no new messages
        return Response([], status=HTTP_200_OK)
        
    new_messages = Message.objects.filter(chat=chat.id).order_by('-timestamp')[:new_amount]

    message_serializer = MessageSerializer(new_messages, many=True)

    return Response(message_serializer.data, status=HTTP_200_OK)





# not in use for now !!!!!!

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