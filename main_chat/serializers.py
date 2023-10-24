from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')  # o los campos que desees incluir


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)  # Añade esta línea

    class Meta:
        model = Chat
        fields = '__all__'