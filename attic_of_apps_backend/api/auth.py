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
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_auth(request):
    _username = request.data.get("username")
    _email = request.data.get("email")
    _password = request.data.get("password")
    if _username is None or _email is None or _password is None:
        return Response({'error': 'Data sent was invalid'}, status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=_username).exists():
        return Response({'error': 'User already exists'}, status=HTTP_404_NOT_FOUND)

    User.objects._create_user(_username, _email, _password)
    return Response({'message', 'Created user: %s' % _username}, status=HTTP_201_CREATED)

@csrf_exempt
@api_view(["POST"])
def get_user(request):
    return Response({ 'user':  json.loads(serializers.serialize('json', [request.user]))[0]['fields']}, status=HTTP_200_OK)    

@csrf_exempt
@api_view(["POST"])
def logout(request):
        request.user.auth_token.delete()
        return Response({'message': 'You have been successfully logged out'}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test_route(request):
    return Response({ 'test':  "test data"}, status=HTTP_200_OK) 
