from .models import Chat, Message
from django.contrib.auth.models import User
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = ['title', 'timestamp']


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField('get_user')
    
    class Meta:
        model = Chat
        fields = ['message', 'sender', 'timestamp']


    def get_user(self, message):

        if hasattr(message, "user"):
            if message.user.first_name and message.user.last_name:
                return f'{message.user.first_name} {message.user.last_name}'        
            
        return None