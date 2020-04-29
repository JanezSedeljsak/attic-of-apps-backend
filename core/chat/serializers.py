from .models import Chat, Message
from django.contrib.auth.models import User
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = ['title', 'timestamp']

class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('sender', 'message', 'chat')


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField('get_user')
    senderEmail = serializers.SerializerMethodField('get_user_email')
    avatarAlt = serializers.SerializerMethodField('get_avatar_alt')
    
    class Meta:
        model = Message
        fields = ['message', 'sender', 'timestamp', 'senderEmail', 'avatarAlt']


    def get_user(self, message):

        if hasattr(message, "sender"):
            if message.sender.first_name and message.sender.last_name:
                return f'{message.sender.first_name} {message.sender.last_name}'        
            
        return None

    def get_user_email(self, message):

        if hasattr(message, "sender"):
            if message.sender.email:
                return f'{message.sender.email}'       
            
        return None

    def get_avatar_alt(self, message):

        if hasattr(message, "sender"):
            if message.sender.first_name and message.sender.last_name:
                firstTwoLetters = f'{message.sender.first_name[0]}{message.sender.last_name[0]}'
                return firstTwoLetters.upper()
