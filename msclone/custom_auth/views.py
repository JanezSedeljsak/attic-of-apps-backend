from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core import serializers
from .serializers import UserSerializer
from django.db.models import Q
import json


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    _username = request.data.get("username")
    _password = request.data.get("password")
    if _username is None or _password is None:
        return Response({'error': 'Data sent was invalid'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=_username, password=_password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)

    user_serializer = UserSerializer(user)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': user_serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_auth(request):
    _username = request.data.get("username")
    _email = request.data.get("email")
    _password = request.data.get("password")
    _first_name = request.data.get("first_name")
    _last_name = request.data.get("last_name")
    if _username is None or _email is None or _password is None or _first_name is None or _last_name is None:
        return Response({'error': 'Data sent was invalid'}, status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(Q(username=_username) | Q(email=_email)).exists():
        return Response({'error': 'User already exists'}, status=HTTP_404_NOT_FOUND)

    User.objects._create_user(
        _username, _email, _password, first_name=_first_name, last_name=_last_name)
    return Response({'message': f'Created user: {_username}'}, status=HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'You have been successfully logged out'}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def heartbeat(request):
    return Response({'running':  True}, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def update_auth(request):
    _username = request.data.get("username")
    _password = request.data.get("old_password")
    del request.data['old_password']

    if _username is None or _password is None:
        return Response({'error': 'Data sent was invalid'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=_username, password=_password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)


    user_serializer = UserSerializer(user, data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
    else:
        return Response({'error': task_serializer.errors}, status=HTTP_400_BAD_REQUEST) 


    return Response({ 'message': 'User credentials were successfully updated'}, status=HTTP_200_OK)
